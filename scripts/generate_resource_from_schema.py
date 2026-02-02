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
from typing import Any, Dict, Optional, Set, Tuple

import httpx

SCHEMA_URL_TEMPLATE = "https://schema.cloudformation.{region}.amazonaws.com/CloudformationSchema.zip"
DEFAULT_REGION = "us-east-1"

# Cache for downloaded schemas
_schemas_cache: Optional[Dict[str, Any]] = None


def download_schemas(region: str = DEFAULT_REGION) -> Dict[str, Any]:
    """Download all CloudFormation schemas for a region."""
    global _schemas_cache
    if _schemas_cache is not None:
        return _schemas_cache

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

    _schemas_cache = schemas
    print(f"Downloaded {len(schemas)} schemas", file=sys.stderr)
    return schemas


def get_schema(resource_type: str, region: str = DEFAULT_REGION) -> Dict[str, Any]:
    """Get the schema for a specific resource type."""
    schemas = download_schemas(region)
    if resource_type not in schemas:
        available = [t for t in schemas.keys() if resource_type.split("::")[-1] in t]
        raise ValueError(
            f"Resource type '{resource_type}' not found in schema registry.\n"
            f"Similar types: {available[:10]}"
        )
    return schemas[resource_type]


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
    # Some services use acronyms (IAM, EC2), others use CamelCase
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


def json_type_to_python_type(
    json_type: Optional[str],
    property_schema: Dict[str, Any],
    definitions: Dict[str, Any],
    property_name: str,
    is_required: bool,
) -> Tuple[str, Set[str]]:
    """
    Convert JSON schema type to Python type annotation.

    Returns (type_annotation, set of imports needed)
    """
    imports = set()

    # Handle $ref
    if "$ref" in property_schema:
        ref = property_schema["$ref"]
        if ref.startswith("#/definitions/"):
            # For complex nested types, use ResolvableGeneric
            imports.add("from pycfmodel.model.generic import ResolvableGeneric")
            return "ResolvableGeneric", imports

    # Handle anyOf/oneOf
    if "anyOf" in property_schema or "oneOf" in property_schema:
        variants = property_schema.get("anyOf") or property_schema.get("oneOf", [])
        for variant in variants:
            if variant.get("type") == "array":
                imports.add("from typing import List")
                imports.add("from pycfmodel.model.generic import ResolvableGeneric")
                imports.add("from pycfmodel.model.types import Resolvable")
                return "Resolvable[List[ResolvableGeneric]]", imports
        imports.add("from pycfmodel.model.generic import ResolvableGeneric")
        return "ResolvableGeneric", imports

    if json_type is None:
        imports.add("from pycfmodel.model.generic import ResolvableGeneric")
        return "ResolvableGeneric", imports

    # Handle multiple types (e.g., ["string", "object"])
    if isinstance(json_type, list):
        imports.add("from pycfmodel.model.generic import ResolvableGeneric")
        return "ResolvableGeneric", imports

    # Handle array types
    if json_type == "array":
        items = property_schema.get("items", {})
        imports.add("from typing import List")
        imports.add("from pycfmodel.model.types import Resolvable")

        if "$ref" in items:
            imports.add("from pycfmodel.model.generic import ResolvableGeneric")
            return "Resolvable[List[ResolvableGeneric]]", imports

        item_type = items.get("type")
        if item_type == "string":
            imports.add("from pycfmodel.model.types import ResolvableStr")
            return "Resolvable[List[ResolvableStr]]", imports
        elif item_type == "integer":
            imports.add("from pycfmodel.model.types import ResolvableInt")
            return "Resolvable[List[ResolvableInt]]", imports
        elif item_type == "object":
            imports.add("from pycfmodel.model.generic import ResolvableGeneric")
            return "Resolvable[List[ResolvableGeneric]]", imports
        else:
            imports.add("from pycfmodel.model.generic import ResolvableGeneric")
            return "Resolvable[List[ResolvableGeneric]]", imports

    # Simple type mappings
    type_map = {
        "string": ("ResolvableStr", {"from pycfmodel.model.types import ResolvableStr"}),
        "integer": ("ResolvableInt", {"from pycfmodel.model.types import ResolvableInt"}),
        "number": ("ResolvableInt", {"from pycfmodel.model.types import ResolvableInt"}),
        "boolean": ("ResolvableBool", {"from pycfmodel.model.types import ResolvableBool"}),
        "object": ("ResolvableGeneric", {"from pycfmodel.model.generic import ResolvableGeneric"}),
    }

    if json_type in type_map:
        type_str, type_imports = type_map[json_type]
        imports.update(type_imports)
        return type_str, imports

    # Fallback
    imports.add("from pycfmodel.model.generic import ResolvableGeneric")
    return "ResolvableGeneric", imports


def generate_resource_code(resource_type: str, region: str = DEFAULT_REGION) -> str:
    """Generate Python code for a pycfmodel resource."""
    schema = get_schema(resource_type, region)
    class_name, props_class_name, _ = resource_type_to_class_names(resource_type)

    # Extract schema components
    properties = schema.get("properties", {})
    definitions = schema.get("definitions", {})
    required_props = set(schema.get("required", []))
    description = schema.get("description", f"{resource_type} resource")

    # Filter out read-only properties
    read_only = set()
    for prop_path in schema.get("readOnlyProperties", []):
        if prop_path.startswith("/properties/"):
            read_only.add(prop_path.split("/")[-1])
    properties = {k: v for k, v in properties.items() if k not in read_only}

    # Collect imports
    all_imports = {
        "from typing import Literal",
        "from pycfmodel.model.base import CustomModel",
        "from pycfmodel.model.resources.resource import Resource",
        "from pycfmodel.model.types import Resolvable",
    }

    # Generate property fields
    property_fields = []
    has_optional = False
    has_list = False

    for prop_name, prop_schema in sorted(properties.items()):
        is_required = prop_name in required_props
        prop_type = prop_schema.get("type")
        prop_description = prop_schema.get("description", "")

        type_annotation, imports = json_type_to_python_type(
            prop_type, prop_schema, definitions, prop_name, is_required
        )
        all_imports.update(imports)

        if not is_required:
            has_optional = True
            type_annotation = f"Optional[{type_annotation}]"

        if "List" in type_annotation:
            has_list = True

        default = " = None" if not is_required else ""
        property_fields.append((prop_name, type_annotation, default, prop_description))

    if has_optional:
        all_imports.add("from typing import Optional")
    if has_list and "from typing import List" not in all_imports:
        all_imports.add("from typing import List")

    # Sort imports
    typing_imports = sorted([i for i in all_imports if i.startswith("from typing")])
    pycfmodel_imports = sorted([i for i in all_imports if i.startswith("from pycfmodel")])

    # Generate code
    lines = ['"""']
    lines.append(f"{class_name} resource for AWS CloudFormation.")
    lines.append("")
    lines.append(f"Auto-generated from AWS CloudFormation schema for {resource_type}.")
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

    # Properties class
    lines.append(f"class {props_class_name}(CustomModel):")
    lines.append('    """')
    lines.append(f"    Properties for {resource_type}.")
    lines.append("")
    lines.append("    Properties:")
    lines.append("")
    for prop_name, _, _, prop_desc in property_fields:
        short_desc = prop_desc[:80] + "..." if len(prop_desc) > 80 else prop_desc
        lines.append(f"    - {prop_name}: {short_desc}")
    lines.append("")
    lines.append(f"    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-{resource_type.lower().replace('::', '-').replace('aws-', '')}.html)")
    lines.append('    """')
    lines.append("")

    # Sort fields: required first, then optional
    required_fields = [(n, t, d, desc) for n, t, d, desc in property_fields if d == ""]
    optional_fields = [(n, t, d, desc) for n, t, d, desc in property_fields if d != ""]

    for prop_name, type_annotation, default, _ in required_fields + optional_fields:
        lines.append(f"    {prop_name}: {type_annotation}{default}")

    if not property_fields:
        lines.append("    pass")

    lines.append("")
    lines.append("")

    # Resource class
    lines.append(f"class {class_name}(Resource):")
    lines.append('    """')
    lines.append(f"    {description}")
    lines.append("")
    lines.append("    Properties:")
    lines.append("")
    lines.append(f"    - Properties: A [{props_class_name}][pycfmodel.model.resources.{resource_type_to_class_names(resource_type)[2][:-3]}.{props_class_name}] object.")
    lines.append("")
    lines.append(f"    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-{resource_type.lower().replace('::', '-').replace('aws-', '')}.html)")
    lines.append('    """')
    lines.append("")
    lines.append(f'    Type: Literal["{resource_type}"]')

    # Determine if Properties should be Optional
    has_required_props = any(d == "" for _, _, d, _ in property_fields)
    if has_required_props:
        lines.append(f"    Properties: Resolvable[{props_class_name}]")
    else:
        lines.append(f"    Properties: Optional[Resolvable[{props_class_name}]] = None")

    lines.append("")

    return "\n".join(lines)


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
        schemas = download_schemas(args.region)
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
