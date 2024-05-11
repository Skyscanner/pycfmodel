import logging
from typing import Optional

from pydantic import ConfigDict, field_validator

from pycfmodel.model.generic import Generic
from pycfmodel.model.resources.resource import Resource

logger = logging.getLogger(__file__)


class GenericResource(Resource):
    """This class is used for all resource types that don't have a dedicated class."""

    Type: str
    Properties: Optional[Generic] = None

    model_config = ConfigDict(extra="allow")

    @field_validator("Type", mode="before")
    @classmethod
    def check_type(cls, value, values, **kwargs):
        from pycfmodel.model.resources.types import ResourceModels

        existing_resource_types = {
            klass.model_fields["Type"].annotation.__args__[0] for klass in ResourceModels.__args__[0].__args__
        }
        if value in existing_resource_types:
            logger.warning(f"Instantiating a GenericResource from a {value} in {values}")
        return value
