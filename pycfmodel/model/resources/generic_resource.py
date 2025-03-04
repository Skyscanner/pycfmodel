import logging
from typing import ClassVar, Optional

from pydantic import ConfigDict, field_validator

from pycfmodel.model.generic import Generic
from pycfmodel.model.resources.resource import Resource

logger = logging.getLogger(__name__)


class GenericResource(Resource):
    """This class is used for all resource types that don't have a dedicated class."""

    Type: Optional[str] = None  # Optional to handle cases like "AWS::CloudFormation::Authentication"
    Properties: Optional[Generic] = None

    model_config = ConfigDict(extra="allow")
    _strict: ClassVar[bool] = True

    @field_validator("Type", mode="before")
    @classmethod
    def check_type(cls, value, values, **kwargs):
        from pycfmodel.model.resources.types import ResourceModels

        existing_resource_types = {
            klass.model_fields["Type"].annotation.__args__[0] for klass in ResourceModels.__args__[0].__args__
        }
        if value in existing_resource_types and cls._strict:
            raise ValueError(f"Instantiation of GenericResource from {value} in {values} not allowed")
        else:
            logger.warning(f"Instantiation of GenericResource from {value} in {values}")
        return value
