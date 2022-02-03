import logging
from typing import ClassVar

from pydantic import Extra, validator

from pycfmodel.model.generic import Generic
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.resources.types import ResourceModels

logger = logging.getLogger(__file__)

_EXISTING_RESOURCE_TYPES = {klass.TYPE_VALUE for klass in ResourceModels.__args__}


class GenericResource(Resource):
    """This class is used for all resource types that don't have a dedicated class."""

    ALLOW_EXISTING_TYPES: ClassVar[bool] = True
    Type: str
    Properties: Generic

    class Config(Resource.Config):
        extra = Extra.allow

    @validator("Type", pre=True)
    def check_type(cls, value, values, **kwargs):
        if value in _EXISTING_RESOURCE_TYPES:
            if cls.ALLOW_EXISTING_TYPES:
                logger.warning(f"Instantiating a GenericResource from a {value} in {values}")
            else:
                raise ValueError(f"Instantiation of GenericResource from {value} in {values} not allowed")
        return value
