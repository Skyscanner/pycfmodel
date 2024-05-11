from typing import Optional

from pydantic import ConfigDict, field_validator

from pycfmodel.model.generic import Generic
from pycfmodel.model.resources.resource import Resource


class GenericResource(Resource):
    """This class is used for all resource types that don't have a dedicated class."""

    Type: Optional[str] = None  # Optional to handle cases like "AWS::CloudFormation::Authentication"
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
            raise ValueError(f"Instantiation of GenericResource from {value} in {values} not allowed")
        return value
