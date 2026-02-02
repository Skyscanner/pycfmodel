"""
Dynamically generate pycfmodel resource classes from AWS CloudFormation schemas.
"""

import io
import json
import zipfile
from functools import lru_cache
from typing import Any, Dict, List, Literal, Optional, Type, Union

import httpx
from pydantic import create_model

from pycfmodel.model.base import CustomModel, FunctionDict
from pycfmodel.model.generic import Generic
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableStr

SCHEMA_URL_TEMPLATE = "https://schema.cloudformation.{region}.amazonaws.com/CloudformationSchema.zip"
DEFAULT_REGION = "us-east-1"


@lru_cache(maxsize=1)
def _download_schemas(region: str = DEFAULT_REGION) -> Dict[str, Any]:
    """Download and cache all CloudFormation schemas for a region."""
    url = SCHEMA_URL_TEMPLATE.format(region=region)
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

    return schemas


def get_schema_for_resource(resource_type: str, region: str = DEFAULT_REGION) -> Optional[Dict[str, Any]]:
    """
    Get the CloudFormation schema for a specific resource type.

    Args:
        resource_type: The CloudFormation resource type (e.g., "AWS::S3::Bucket")
        region: AWS region to fetch schemas from

    Returns:
        The schema dictionary or None if not found
    """
    schemas = _download_schemas(region)
    return schemas.get(resource_type)


def _json_type_to_python(
    json_type: Union[str, List[str], None],
    schema_property: Dict[str, Any],
    definitions: Dict[str, Any],
    property_name: str,
) -> Type:
    """Convert a JSON schema type to a Python/Pydantic type."""
    if json_type is None:
        # Check for $ref
        if "$ref" in schema_property:
            return _resolve_ref(schema_property["$ref"], definitions)
        # Check for anyOf/oneOf - try to extract array type if present
        if "anyOf" in schema_property or "oneOf" in schema_property:
            variants = schema_property.get("anyOf") or schema_property.get("oneOf", [])
            for variant in variants:
                if variant.get("type") == "array":
                    # Found an array variant - use List[Generic]
                    return Resolvable[List[Generic]]
            return Resolvable[Generic]
        return Resolvable[Generic]

    if isinstance(json_type, list):
        # Multiple types allowed - use Generic
        return Resolvable[Generic]

    type_mapping = {
        "string": ResolvableStr,
        "integer": ResolvableInt,
        "number": Resolvable[Union[int, float]],
        "boolean": ResolvableBool,
        "object": Resolvable[Generic],
        "array": Resolvable[List[Generic]],
    }

    base_type = type_mapping.get(json_type, Resolvable[Generic])

    # Handle arrays with specific item types
    if json_type == "array" and "items" in schema_property:
        items = schema_property["items"]
        if "$ref" in items:
            item_type = _resolve_ref(items["$ref"], definitions)
            return Resolvable[List[item_type]]
        item_type = _json_type_to_python(items.get("type"), items, definitions, property_name)
        # Unwrap Resolvable for list items
        if hasattr(item_type, "__origin__") and item_type.__origin__ is Union:
            args = item_type.__args__
            if len(args) == 2 and args[1] is FunctionDict:
                item_type = args[0]
        return Resolvable[List[item_type]]

    return base_type


def _resolve_ref(ref: str, definitions: Dict[str, Any]) -> Type:
    """Resolve a $ref to a type."""
    # References are in format "#/definitions/DefinitionName"
    if ref.startswith("#/definitions/"):
        def_name = ref.split("/")[-1]
        if def_name in definitions:
            # For nested definitions, we use Generic to avoid complex recursive types
            return Generic
    return Generic


def _create_properties_model(
    resource_type: str,
    properties: Dict[str, Any],
    definitions: Dict[str, Any],
    required_props: List[str],
) -> Type[CustomModel]:
    """Create a Pydantic model for resource properties."""
    # Convert resource type to class name: AWS::S3::Bucket -> S3BucketProperties
    parts = resource_type.split("::")
    class_name = "".join(parts[1:]) + "Properties"

    field_definitions = {}
    for prop_name, prop_schema in properties.items():
        python_type = _json_type_to_python(
            prop_schema.get("type"),
            prop_schema,
            definitions,
            prop_name,
        )

        # Make optional if not required
        if prop_name not in required_props:
            field_definitions[prop_name] = (Optional[python_type], None)
        else:
            field_definitions[prop_name] = (python_type, ...)

    return create_model(
        class_name,
        __base__=CustomModel,
        __module__="pycfmodel.schema_generator.generated",
        **field_definitions,
    )


def generate_resource_from_schema(
    resource_type: str,
    region: str = DEFAULT_REGION,
) -> Type[Resource]:
    """
    Dynamically generate a pycfmodel Resource class from an AWS CloudFormation schema.

    Args:
        resource_type: The CloudFormation resource type (e.g., "AWS::S3::Bucket")
        region: AWS region to fetch schemas from

    Returns:
        A dynamically generated Resource subclass

    Raises:
        ValueError: If the resource type is not found in the schema registry

    Example:
        >>> DynamicLambdaFunction = generate_resource_from_schema("AWS::Lambda::Function")
        >>> resource = DynamicLambdaFunction(
        ...     Type="AWS::Lambda::Function",
        ...     Properties={"FunctionName": "my-function", "Runtime": "python3.9", ...}
        ... )
    """
    schema = get_schema_for_resource(resource_type, region)
    if schema is None:
        raise ValueError(f"Resource type '{resource_type}' not found in CloudFormation schema registry")

    # Extract schema components
    properties = schema.get("properties", {})
    definitions = schema.get("definitions", {})
    required_props = schema.get("required", [])

    # Filter out read-only properties (they can't be set by users)
    read_only = set()
    for prop_path in schema.get("readOnlyProperties", []):
        # Format is /properties/PropertyName
        if prop_path.startswith("/properties/"):
            read_only.add(prop_path.split("/")[-1])

    # Remove read-only properties from properties dict
    properties = {k: v for k, v in properties.items() if k not in read_only}

    # Create the Properties model
    properties_model = _create_properties_model(
        resource_type,
        properties,
        definitions,
        required_props,
    )

    # Create resource class name: AWS::S3::Bucket -> S3Bucket
    parts = resource_type.split("::")
    resource_class_name = "".join(parts[1:])

    # Create the Resource model
    resource_model = create_model(
        resource_class_name,
        __base__=Resource,
        __module__="pycfmodel.schema_generator.generated",
        Type=(Literal[resource_type], ...),
        Properties=(Optional[Resolvable[properties_model]], None),
    )

    # Store metadata
    resource_model._schema = schema
    resource_model._properties_model = properties_model

    return resource_model
