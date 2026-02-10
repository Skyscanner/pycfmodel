#!/usr/bin/env python3
"""
Generate pycfmodel resource classes from AWS CloudFormation schemas.

This script creates static Python files that can be integrated into the
pycfmodel codebase permanently, following the existing patterns and conventions.

Usage:
    python scripts/generate_resource_from_schema.py AWS::Lambda::Function
    python scripts/generate_resource_from_schema.py AWS::Lambda::Function --output-dir pycfmodel/model/resources
    python scripts/generate_resource_from_schema.py AWS::Lambda::Function --dry-run

The generated files follow the existing pycfmodel conventions:
- Properties class with Optional fields for each property
- Resource class inheriting from Resource base class
- Nested definition classes for complex types (e.g., AvailabilityZoneImpairmentPolicy)
- Proper type annotations using Resolvable, ResolvableStr, etc.
- Docstrings with AWS documentation links
"""

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import httpx

SCHEMA_URL_TEMPLATE = "https://schema.cloudformation.{region}.amazonaws.com/CloudformationSchema.zip"
DEFAULT_REGION = "us-east-1"


class SchemaRegistry:
    """Downloads and caches CloudFormation schemas from AWS."""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def download_schemas(self, region: str = DEFAULT_REGION) -> Dict[str, Any]:
        """Download all CloudFormation schemas for a region."""
        if region in self._cache:
            return self._cache[region]

        url = SCHEMA_URL_TEMPLATE.format(region=region)
        print(f"Downloading schemas from {url}...", file=sys.stderr)
        response = httpx.get(url, timeout=60.0)
        response.raise_for_status()

        schemas = {}
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            for name in zf.namelist():
                if name.endswith(".json"):
                    with zf.open(name) as f:
                        schema = json.load(f)
                        type_name = schema.get("typeName", "")
                        if type_name:
                            schemas[type_name] = schema

        self._cache[region] = schemas
        print(f"Downloaded {len(schemas)} schemas", file=sys.stderr)
        return schemas

    def get_schema(self, resource_type: str, region: str = DEFAULT_REGION) -> Dict[str, Any]:
        """Get the schema for a specific resource type."""
        schemas = self.download_schemas(region)
        if resource_type not in schemas:
            available = [t for t in schemas.keys() if resource_type.split("::")[-1] in t]
            raise ValueError(
                f"Resource type '{resource_type}' not found in schema registry.\n" f"Similar types: {available[:10]}"
            )
        return schemas[resource_type]


# Default registry instance for module-level functions
_registry = SchemaRegistry()


def get_schema(resource_type: str, region: str = DEFAULT_REGION) -> Dict[str, Any]:
    """Get the schema for a specific resource type."""
    return _registry.get_schema(resource_type, region)


def resource_type_to_class_names(resource_type: str) -> Tuple[str, str, str]:
    """
    Convert resource type to class names.

    AWS::Lambda::Function -> (LambdaFunction, LambdaFunctionProperties, lambda_function.py)
    AWS::EC2::SecurityGroup -> (EC2SecurityGroup, EC2SecurityGroupProperties, ec2_security_group.py)
    AWS::IAM::Role -> (IAMRole, IAMRoleProperties, iam_role.py)
    AWS::DynamoDB::Table -> (DynamoDBTable, DynamoDBTableProperties, dynamodb_table.py)
    """
    parts = resource_type.split("::")
    if len(parts) != 3:
        raise ValueError(f"Invalid resource type format: {resource_type}")

    service, resource = parts[1], parts[2]

    # Map service names to their canonical forms for class names
    service_class_map = {
        "IAM": "IAM",
        "EC2": "EC2",
        "RDS": "RDS",
        "SQS": "SQS",
        "SNS": "SNS",
        "KMS": "KMS",
        "ECS": "ECS",
        "ECR": "ECR",
        "EFS": "EFS",
        "EMR": "EMR",
        "SSM": "SSM",
        "WAF": "WAF",
        "ACM": "ACM",
        "DynamoDB": "DynamoDB",
        "CloudWatch": "CloudWatch",
        "Route53": "Route53",
        "AutoScaling": "AutoScaling",
        "ElasticLoadBalancingV2": "ELBv2",
        "ElasticLoadBalancing": "ELB",
        "ElastiCache": "ElastiCache",
        "ApplicationAutoScaling": "ApplicationAutoScaling",
        "Lambda": "Lambda",
        "ApiGateway": "ApiGateway",
        "CloudFormation": "CloudFormation",
        "Logs": "Logs",
        "Events": "Events",
        "Glue": "Glue",
        "CodeBuild": "CodeBuild",
        "StepFunctions": "StepFunctions",
        "SecretsManager": "SecretsManager",
    }

    # Map service names to their filename prefixes
    service_file_map = {
        "IAM": "iam",
        "EC2": "ec2",
        "RDS": "rds",
        "SQS": "sqs",
        "SNS": "sns",
        "KMS": "kms",
        "ECS": "ecs",
        "ECR": "ecr",
        "EFS": "efs",
        "EMR": "emr",
        "SSM": "ssm",
        "WAF": "waf",
        "ACM": "acm",
        "DynamoDB": "dynamodb",
        "CloudWatch": "cloudwatch",
        "Route53": "route53",
        "AutoScaling": "autoscaling",
        "ElasticLoadBalancingV2": "elbv2",
        "ElasticLoadBalancing": "elb",
        "ElastiCache": "elasticache",
        "ApplicationAutoScaling": "application_autoscaling",
        "Lambda": "lambda",
        "ApiGateway": "apigateway",
        "CloudFormation": "cloudformation",
        "Logs": "logs",
        "Events": "events",
        "Glue": "glue",
        "CodeBuild": "codebuild",
        "StepFunctions": "stepfunctions",
        "SecretsManager": "secretsmanager",
    }

    service_class = service_class_map.get(service, service)
    service_file = service_file_map.get(service, service.lower())

    class_name = f"{service_class}{resource}"
    properties_class_name = f"{class_name}Properties"

    # Convert resource name to snake_case for filename
    resource_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", resource).lower()
    filename = f"{service_file}_{resource_snake}.py"

    return class_name, properties_class_name, filename


class CodeGenerator:
    """Generates Python code for CloudFormation resources with nested types."""

    # Definitions that should use existing pycfmodel types instead of being generated
    REUSE_EXISTING_TYPES = {
        "Tag": ("from pycfmodel.model.resources.properties.tag import Tag", "Tag"),
    }

    def __init__(self, resource_type: str, schema: Dict[str, Any]):
        self.resource_type = resource_type
        self.schema = schema
        self.definitions = schema.get("definitions", {})
        self.properties = schema.get("properties", {})
        self.required_props = set(schema.get("required", []))
        self.description = schema.get("description", f"{resource_type} resource")

        # Filter out read-only properties
        read_only = set()
        for prop_path in schema.get("readOnlyProperties", []):
            if prop_path.startswith("/properties/"):
                read_only.add(prop_path.split("/")[-1])
        self.properties = {k: v for k, v in self.properties.items() if k not in read_only}

        # Track which definitions we need to generate
        self.needed_definitions: Set[str] = set()
        self.generated_definitions: Set[str] = set()

        # Track dependencies between definitions for topological sorting
        self.definition_dependencies: Dict[str, Set[str]] = {}

        # Imports
        self.imports: Set[str] = {
            "from typing import Literal",
            "from pycfmodel.model.base import CustomModel",
            "from pycfmodel.model.resources.resource import Resource",
            "from pycfmodel.model.types import Resolvable",
        }

        # Class name info
        class_name, props_class_name, _ = resource_type_to_class_names(resource_type)
        self.class_name = class_name
        self.props_class_name = props_class_name

    def get_type_for_schema(
        self,
        prop_schema: Dict[str, Any],
        is_required: bool,
        context: str = "",
    ) -> str:
        """Convert a JSON schema to a Python type annotation."""
        # Handle $ref to definitions
        if "$ref" in prop_schema:
            ref = prop_schema["$ref"]
            if ref.startswith("#/definitions/"):
                def_name = ref.split("/")[-1]

                # Check if we should reuse an existing pycfmodel type
                if def_name in self.REUSE_EXISTING_TYPES:
                    import_stmt, type_name = self.REUSE_EXISTING_TYPES[def_name]
                    self.imports.add(import_stmt)
                    return type_name

                # Check if the definition is actually an object with properties
                # If it's an array or primitive type, inline it instead of generating a class
                definition = self.definitions.get(def_name, {})
                def_type = definition.get("type")
                if def_type == "array":
                    # Inline the array type
                    items = definition.get("items", {})
                    item_type = self._get_item_type(items)
                    self.imports.add("from typing import List")
                    return f"Resolvable[List[{item_type}]]"
                elif def_type in ("string", "integer", "number", "boolean"):
                    # Inline primitive types
                    type_map = {
                        "string": "ResolvableStr",
                        "integer": "ResolvableInt",
                        "number": "ResolvableInt",
                        "boolean": "ResolvableBool",
                    }
                    type_str = type_map[def_type]
                    if type_str == "ResolvableStr":
                        self.imports.add("from pycfmodel.model.types import ResolvableStr")
                    elif type_str == "ResolvableInt":
                        self.imports.add("from pycfmodel.model.types import ResolvableInt")
                    elif type_str == "ResolvableBool":
                        self.imports.add("from pycfmodel.model.types import ResolvableBool")
                    return type_str
                elif def_type == "object" or definition.get("properties"):
                    # Generate a nested model class and use ResolvableModel
                    self.needed_definitions.add(def_name)
                    self.imports.add("from pycfmodel.model.types import ResolvableModel")
                    return f"Resolvable{def_name}"
                else:
                    # Unknown or complex type, fall back to Resolvable[dict]
                    return "Resolvable[dict]"

        # Handle anyOf/oneOf
        if "anyOf" in prop_schema or "oneOf" in prop_schema:
            variants = prop_schema.get("anyOf") or prop_schema.get("oneOf", [])
            # Check if any variant is an array
            for variant in variants:
                if variant.get("type") == "array":
                    items = variant.get("items", {})
                    item_type = self._get_item_type(items)
                    self.imports.add("from typing import List")
                    return f"Resolvable[List[{item_type}]]"
            # Check for $ref in variants
            for variant in variants:
                if "$ref" in variant:
                    ref = variant["$ref"]
                    if ref.startswith("#/definitions/"):
                        def_name = ref.split("/")[-1]
                        definition = self.definitions.get(def_name, {})
                        if definition.get("type") == "object" or definition.get("properties"):
                            # Generate a nested model class and use ResolvableModel
                            self.needed_definitions.add(def_name)
                            self.imports.add("from pycfmodel.model.types import ResolvableModel")
                            return f"Resolvable{def_name}"
                        else:
                            # Fall back to inline handling
                            return self.get_type_for_schema(variant, is_required, context)
            return "Resolvable[dict]"

        json_type = prop_schema.get("type")

        if json_type is None:
            return "Resolvable[dict]"

        # Handle multiple types (e.g., ["string", "object"])
        if isinstance(json_type, list):
            return "Resolvable[dict]"

        # Handle array types
        if json_type == "array":
            items = prop_schema.get("items", {})
            item_type = self._get_item_type(items)
            self.imports.add("from typing import List")
            return f"Resolvable[List[{item_type}]]"

        # Simple type mappings
        type_map = {
            "string": "ResolvableStr",
            "integer": "ResolvableInt",
            "number": "ResolvableInt",
            "boolean": "ResolvableBool",
            "object": "Resolvable[dict]",
        }

        if json_type in type_map:
            type_str = type_map[json_type]
            if type_str == "ResolvableStr":
                self.imports.add("from pycfmodel.model.types import ResolvableStr")
            elif type_str == "ResolvableInt":
                self.imports.add("from pycfmodel.model.types import ResolvableInt")
            elif type_str == "ResolvableBool":
                self.imports.add("from pycfmodel.model.types import ResolvableBool")
            return type_str

        # Fallback
        return "Resolvable[dict]"

    def _get_item_type(self, items: Dict[str, Any]) -> str:
        """Get the type for array items."""
        if "$ref" in items:
            ref = items["$ref"]
            if ref.startswith("#/definitions/"):
                def_name = ref.split("/")[-1]

                # Check if we should reuse an existing pycfmodel type
                if def_name in self.REUSE_EXISTING_TYPES:
                    import_stmt, type_name = self.REUSE_EXISTING_TYPES[def_name]
                    self.imports.add(import_stmt)
                    return type_name

                definition = self.definitions.get(def_name, {})
                if definition.get("type") == "object" or definition.get("properties"):
                    # Generate a nested model class for array items
                    self.needed_definitions.add(def_name)
                    return def_name
                elif definition.get("type") == "array":
                    # Inline nested arrays
                    nested_items = definition.get("items", {})
                    return self._get_item_type(nested_items)
                else:
                    return "dict"

        item_type = items.get("type")
        if item_type == "string":
            self.imports.add("from pycfmodel.model.types import ResolvableStr")
            return "ResolvableStr"
        elif item_type == "integer":
            self.imports.add("from pycfmodel.model.types import ResolvableInt")
            return "ResolvableInt"
        else:
            # For object or unknown types, use dict
            return "dict"

    def get_definition_dependencies(self, def_name: str) -> Set[str]:
        """Get the set of definitions that this definition depends on."""
        if def_name in self.definition_dependencies:
            return self.definition_dependencies[def_name]

        deps: Set[str] = set()
        definition = self.definitions.get(def_name, {})
        if not definition:
            self.definition_dependencies[def_name] = deps
            return deps

        # Check properties for $ref
        props = definition.get("properties", {})
        for prop_schema in props.values():
            self._collect_refs(prop_schema, deps)

        # Also check array items for $ref
        if "items" in definition:
            self._collect_refs(definition["items"], deps)

        self.definition_dependencies[def_name] = deps
        return deps

    def _collect_refs(self, schema: Dict[str, Any], refs: Set[str]) -> None:
        """Recursively collect all $ref definitions from a schema."""
        if "$ref" in schema:
            ref = schema["$ref"]
            if ref.startswith("#/definitions/"):
                refs.add(ref.split("/")[-1])
        if "items" in schema:
            self._collect_refs(schema["items"], refs)
        for key in ("anyOf", "oneOf"):
            if key in schema:
                for variant in schema[key]:
                    self._collect_refs(variant, refs)

    def topological_sort_definitions(self, definitions: Set[str]) -> List[str]:
        """Sort definitions topologically so dependencies come first."""
        # Build dependency graph
        for def_name in definitions:
            self.get_definition_dependencies(def_name)

        # Kahn's algorithm for topological sort
        in_degree: Dict[str, int] = {d: 0 for d in definitions}
        for def_name in definitions:
            for dep in self.definition_dependencies.get(def_name, set()):
                if dep in definitions:
                    in_degree[def_name] += 1

        # Start with nodes that have no dependencies
        queue = [d for d in definitions if in_degree[d] == 0]
        result = []

        while queue:
            # Sort queue for deterministic output
            queue.sort()
            node = queue.pop(0)
            result.append(node)

            # For each definition that depends on this node
            for def_name in definitions:
                if node in self.definition_dependencies.get(def_name, set()):
                    in_degree[def_name] -= 1
                    if in_degree[def_name] == 0:
                        queue.append(def_name)

        # If there are cycles, add remaining definitions in alphabetical order
        remaining = set(definitions) - set(result)
        result.extend(sorted(remaining))

        return result

    def should_generate_class(self, def_name: str) -> bool:
        """Check if this definition should become a class (vs being inlined)."""
        # Don't generate classes for types we reuse from pycfmodel
        if def_name in self.REUSE_EXISTING_TYPES:
            return False

        definition = self.definitions.get(def_name, {})
        if not definition:
            return False
        def_type = definition.get("type")
        # Only generate classes for objects with properties
        if def_type == "object" or definition.get("properties"):
            return True
        return False

    def _detect_field_name_shadowing(self, fields: List[Tuple[str, str, str, bool]]) -> Dict[str, str]:
        """
        Detect fields whose names shadow class names used in List[] annotations of sibling fields.

        When a class has a field like `Transition: Optional[...] = None` and another field
        `Transitions: Optional[Resolvable[List[Transition]]] = None`, Python evaluates the
        List[Transition] annotation inside the class body where `Transition` has already been
        set to None (the default value), causing List[Transition] to resolve to List[NoneType].

        Returns a dict mapping class names to their pre-resolved type alias names.
        """
        field_names = {name for name, _, _, _ in fields}
        aliases = {}

        for _, type_annotation, _, _ in fields:
            # Find all List[ClassName] patterns in the annotation
            match = re.search(r"Resolvable\[List\[(\w+)\]\]", type_annotation)
            if match:
                class_name = match.group(1)
                if class_name in field_names and class_name not in aliases:
                    alias_name = f"_{class_name}List"
                    aliases[class_name] = alias_name

        return aliases

    def _apply_shadowing_aliases(
        self, fields: List[Tuple[str, str, str, bool]], aliases: Dict[str, str]
    ) -> List[Tuple[str, str, str, bool]]:
        """Replace Resolvable[List[ClassName]] with the pre-resolved alias in field annotations."""
        if not aliases:
            return fields

        result = []
        for name, type_annotation, default, is_required in fields:
            for class_name, alias_name in aliases.items():
                type_annotation = type_annotation.replace(f"Resolvable[List[{class_name}]]", alias_name)
            result.append((name, type_annotation, default, is_required))
        return result

    def _generate_shadowing_alias_lines(self, aliases: Dict[str, str], class_name: str) -> List[str]:
        """Generate module-level type alias lines to avoid class body name shadowing."""
        lines = []
        for original_class, alias_name in sorted(aliases.items()):
            lines.append(
                f"# Pre-resolved list type to avoid class body name shadowing in {class_name}."
            )
            lines.append(
                f"# The {class_name} class has a field named \"{original_class}\" (default None) which shadows"
            )
            lines.append(
                f"# the {original_class} class when Python evaluates List[{original_class}] inside the class body."
            )
            lines.append(f"{alias_name} = Resolvable[List[{original_class}]]")
            lines.append("")
            lines.append("")
        return lines

    def generate_definition_class(self, def_name: str) -> List[str]:
        """Generate a class for a schema definition."""
        if def_name in self.generated_definitions:
            return []
        self.generated_definitions.add(def_name)

        definition = self.definitions.get(def_name, {})
        if not definition:
            return []

        # Skip non-object definitions (arrays, primitives)
        if not self.should_generate_class(def_name):
            return []

        props = definition.get("properties", {})
        required = set(definition.get("required", []))
        desc = definition.get("description", f"{def_name} configuration.")

        # Generate fields
        fields = []
        for prop_name, prop_schema in sorted(props.items()):
            is_required = prop_name in required
            type_annotation = self.get_type_for_schema(prop_schema, is_required, def_name)

            if not is_required:
                type_annotation = f"Optional[{type_annotation}]"
                self.imports.add("from typing import Optional")

            default = "" if is_required else " = None"
            fields.append((prop_name, type_annotation, default, is_required))

        # Detect and fix field name shadowing in List[] annotations
        aliases = self._detect_field_name_shadowing(fields)
        fields = self._apply_shadowing_aliases(fields, aliases)

        lines = []

        # Emit module-level type aliases before the class to avoid shadowing
        lines.extend(self._generate_shadowing_alias_lines(aliases, def_name))

        lines.append(f"class {def_name}(CustomModel):")
        lines.append('    """')
        # Truncate description to first sentence or 200 chars
        short_desc = desc.split(".")[0] + "." if "." in desc else desc[:200]
        lines.append(f"    {short_desc}")
        lines.append('    """')
        lines.append("")

        # Sort: required first, then optional
        required_fields = [(n, t, d) for n, t, d, r in fields if r]
        optional_fields = [(n, t, d) for n, t, d, r in fields if not r]

        for prop_name, type_annotation, default in required_fields + optional_fields:
            lines.append(f"    {prop_name}: {type_annotation}{default}")

        if not fields:
            lines.append("    pass")

        lines.append("")
        lines.append("")
        # Add the type alias immediately after the class
        # This needs ResolvableModel import
        self.imports.add("from pycfmodel.model.types import ResolvableModel")
        lines.append(f"Resolvable{def_name} = ResolvableModel({def_name})")
        lines.append("")
        lines.append("")

        return lines

    def generate(self) -> str:
        """Generate the complete Python code for the resource."""
        # First pass: collect all needed definitions from properties
        property_fields = []
        for prop_name, prop_schema in sorted(self.properties.items()):
            is_required = prop_name in self.required_props
            type_annotation = self.get_type_for_schema(prop_schema, is_required)

            if not is_required:
                type_annotation = f"Optional[{type_annotation}]"
                self.imports.add("from typing import Optional")

            default = "" if is_required else " = None"
            prop_desc = prop_schema.get("description", "")
            property_fields.append((prop_name, type_annotation, default, prop_desc, is_required))

        # Collect all needed definition classes (recursively)
        while self.needed_definitions - self.generated_definitions:
            pending = self.needed_definitions - self.generated_definitions
            for def_name in pending:
                # Just mark as generated and collect dependencies
                self.generated_definitions.add(def_name)
                deps = self.get_definition_dependencies(def_name)
                self.needed_definitions.update(deps)

        # Reset generated_definitions for actual code generation
        all_definitions = self.generated_definitions.copy()
        self.generated_definitions = set()

        # Sort definitions topologically and generate code
        definition_code_lines = []
        sorted_defs = self.topological_sort_definitions(all_definitions)
        for def_name in sorted_defs:
            definition_code_lines.extend(self.generate_definition_class(def_name))

        # Build imports
        typing_imports = sorted([i for i in self.imports if i.startswith("from typing")])
        pycfmodel_imports = sorted([i for i in self.imports if i.startswith("from pycfmodel")])

        # Generate code
        lines = ['"""']
        lines.append(f"{self.class_name} resource for AWS CloudFormation.")
        lines.append("")
        lines.append(f"Auto-generated from AWS CloudFormation schema for {self.resource_type}.")
        lines.append('"""')
        lines.append("")

        # Combine typing imports
        typing_names = []
        for imp in typing_imports:
            match = re.search(r"from typing import (.+)", imp)
            if match:
                typing_names.extend(match.group(1).split(", "))
        if typing_names:
            lines.append(f"from typing import {', '.join(sorted(set(typing_names)))}")
        lines.append("")

        for imp in pycfmodel_imports:
            lines.append(imp)
        lines.append("")
        lines.append("")

        # Add definition classes first (they need to be defined before Properties class)
        # Each class is immediately followed by its ResolvableX type alias
        lines.extend(definition_code_lines)

        # Detect and fix field name shadowing in Properties class List[] annotations
        props_fields_for_shadowing = [
            (n, t, d, r) for n, t, d, _, r in property_fields
        ]
        props_aliases = self._detect_field_name_shadowing(props_fields_for_shadowing)
        if props_aliases:
            property_fields = [
                (n, t_new, d, desc, r)
                for (n, _, d, desc, r), (_, t_new, _, _) in zip(
                    property_fields,
                    self._apply_shadowing_aliases(props_fields_for_shadowing, props_aliases),
                )
            ]
            lines.extend(self._generate_shadowing_alias_lines(props_aliases, self.props_class_name))

        # Properties class
        lines.append(f"class {self.props_class_name}(CustomModel):")
        lines.append('    """')
        lines.append(f"    Properties for {self.resource_type}.")
        lines.append("")
        lines.append("    Properties:")
        lines.append("")
        for prop_name, _, _, prop_desc, _ in property_fields:
            short_desc = prop_desc[:80] + "..." if len(prop_desc) > 80 else prop_desc
            lines.append(f"    - {prop_name}: {short_desc}")
        lines.append("")
        lines.append(
            f"    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-{self.resource_type.lower().replace('::', '-').replace('aws-', '')}.html)"
        )
        lines.append('    """')
        lines.append("")

        # Sort fields: required first, then optional
        required_fields = [(n, t, d) for n, t, d, _, r in property_fields if r]
        optional_fields = [(n, t, d) for n, t, d, _, r in property_fields if not r]

        for prop_name, type_annotation, default in required_fields + optional_fields:
            lines.append(f"    {prop_name}: {type_annotation}{default}")

        if not property_fields:
            lines.append("    pass")

        lines.append("")
        lines.append("")

        # Resource class
        lines.append(f"class {self.class_name}(Resource):")
        lines.append('    """')
        # Truncate description
        desc_lines = self.description.split("\n")[0][:200]
        lines.append(f"    {desc_lines}")
        lines.append("")
        lines.append("    Properties:")
        lines.append("")
        lines.append(
            f"    - Properties: A [{self.props_class_name}][pycfmodel.model.resources.{resource_type_to_class_names(self.resource_type)[2][:-3]}.{self.props_class_name}] object."
        )
        lines.append("")
        lines.append(
            f"    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-{self.resource_type.lower().replace('::', '-').replace('aws-', '')}.html)"
        )
        lines.append('    """')
        lines.append("")
        lines.append(f'    Type: Literal["{self.resource_type}"]')

        # Determine if Properties should be Optional
        has_required_props = any(r for _, _, _, _, r in property_fields)
        if has_required_props:
            lines.append(f"    Properties: Resolvable[{self.props_class_name}]")
        else:
            lines.append(f"    Properties: Optional[Resolvable[{self.props_class_name}]] = None")

        lines.append("")

        return "\n".join(lines)


def generate_resource_code(resource_type: str, region: str = DEFAULT_REGION) -> str:
    """Generate Python code for a pycfmodel resource."""
    schema = get_schema(resource_type, region)
    generator = CodeGenerator(resource_type, schema)
    return generator.generate()


def main():
    parser = argparse.ArgumentParser(
        description="Generate pycfmodel resource classes from AWS CloudFormation schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s AWS::Lambda::Function
    %(prog)s AWS::Lambda::Function --output-dir pycfmodel/model/resources
    %(prog)s AWS::Lambda::Function --dry-run
    %(prog)s AWS::DynamoDB::Table AWS::SQS::Queue --output-dir pycfmodel/model/resources
        """,
    )
    parser.add_argument(
        "resource_types",
        nargs="*",
        help="CloudFormation resource type(s) to generate (e.g., AWS::Lambda::Function)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        help="Output directory for generated files. If not specified, prints to stdout.",
    )
    parser.add_argument(
        "--region",
        "-r",
        default=DEFAULT_REGION,
        help=f"AWS region to fetch schemas from (default: {DEFAULT_REGION})",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be generated without writing files",
    )
    parser.add_argument(
        "--list-types",
        "-l",
        action="store_true",
        help="List all available resource types",
    )

    args = parser.parse_args()

    if args.list_types:
        schemas = _registry.download_schemas(args.region)
        for resource_type in sorted(schemas.keys()):
            print(resource_type)
        return 0

    if not args.resource_types:
        parser.error("resource_types is required unless --list-types is specified")

    for resource_type in args.resource_types:
        try:
            code = generate_resource_code(resource_type, args.region)
            class_name, props_class_name, filename = resource_type_to_class_names(resource_type)

            if args.output_dir:
                output_path = args.output_dir / filename
                if args.dry_run:
                    print(f"Would write to: {output_path}")
                    print("-" * 60)
                    print(code)
                    print("-" * 60)
                else:
                    args.output_dir.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(code)
                    print(f"Generated: {output_path}")
            else:
                print(code)

        except Exception as e:
            print(f"Error generating {resource_type}: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
