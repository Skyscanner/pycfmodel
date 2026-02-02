"""
Schema generator for dynamically creating pycfmodel resources from AWS CloudFormation schemas.
"""

from pycfmodel.schema_generator.generator import generate_resource_from_schema, get_schema_for_resource

__all__ = ["generate_resource_from_schema", "get_schema_for_resource"]
