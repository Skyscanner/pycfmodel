"""
Dynamic resource generation for CloudFormation resource types not explicitly modeled.
"""

import logging
from typing import Any, Dict, Optional, Type

from pycfmodel.model.resources.resource import Resource

logger = logging.getLogger(__name__)

# Cache for dynamically generated resource models
_dynamic_model_cache: Dict[str, Type[Resource]] = {}

# Flag to enable/disable dynamic generation
_dynamic_generation_enabled: bool = False


def enable_dynamic_generation() -> None:
    """
    Enable dynamic resource generation from AWS CloudFormation schemas.

    When enabled, resources with types not explicitly modeled will be
    dynamically generated from the official AWS CloudFormation schemas
    instead of falling back to GenericResource.
    """
    global _dynamic_generation_enabled
    _dynamic_generation_enabled = True


def disable_dynamic_generation() -> None:
    """
    Disable dynamic resource generation.

    When disabled, resources with types not explicitly modeled will
    fall back to GenericResource (default behavior).
    """
    global _dynamic_generation_enabled
    _dynamic_generation_enabled = False


def is_dynamic_generation_enabled() -> bool:
    """Check if dynamic resource generation is enabled."""
    return _dynamic_generation_enabled


def clear_dynamic_model_cache() -> None:
    """Clear the cache of dynamically generated resource models."""
    _dynamic_model_cache.clear()


def get_or_create_dynamic_model(resource_type: str) -> Optional[Type[Resource]]:
    """
    Get or create a dynamically generated model for a resource type.

    Args:
        resource_type: The CloudFormation resource type (e.g., "AWS::Lambda::Function")

    Returns:
        A dynamically generated Resource subclass, or None if generation fails
    """
    if not _dynamic_generation_enabled:
        return None

    # Check cache first
    if resource_type in _dynamic_model_cache:
        return _dynamic_model_cache[resource_type]

    # Try to generate from schema
    try:
        from pycfmodel.schema_generator import generate_resource_from_schema

        model = generate_resource_from_schema(resource_type)
        _dynamic_model_cache[resource_type] = model
        logger.info(f"Dynamically generated model for {resource_type}")
        return model
    except ValueError as e:
        # Resource type not found in schema registry
        logger.debug(f"Could not generate dynamic model for {resource_type}: {e}")
        return None
    except Exception as e:
        # Other errors (network, parsing, etc.)
        logger.warning(f"Error generating dynamic model for {resource_type}: {e}")
        return None


def parse_resource(resource_data: Dict[str, Any]) -> Resource:
    """
    Parse a resource dictionary into an appropriate Resource instance.

    This function first tries to use explicitly modeled resource types,
    then falls back to dynamic generation if enabled, and finally
    uses GenericResource as a last resort.

    Args:
        resource_data: Dictionary containing resource Type and Properties

    Returns:
        A Resource instance (either explicitly modeled, dynamically generated, or generic)
    """
    from pycfmodel.model.resources.types import ResourceModels

    resource_type = resource_data.get("Type")

    # Get the set of explicitly modeled resource types
    existing_resource_types = {
        klass.model_fields["Type"].annotation.__args__[0] for klass in ResourceModels.__args__[0].__args__
    }

    # If it's an explicitly modeled type, let normal parsing handle it
    if resource_type in existing_resource_types:
        return None  # Signal to use normal parsing

    # Try dynamic generation if enabled
    if _dynamic_generation_enabled:
        dynamic_model = get_or_create_dynamic_model(resource_type)
        if dynamic_model is not None:
            try:
                return dynamic_model.model_validate(resource_data)
            except Exception as e:
                logger.warning(f"Failed to parse {resource_type} with dynamic model: {e}")
                # Fall through to GenericResource

    # Fall back to GenericResource
    return None  # Signal to use normal parsing (which will fall back to GenericResource)
