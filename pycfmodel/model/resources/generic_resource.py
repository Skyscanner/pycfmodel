"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import logging
from typing import ClassVar

from pydantic import Extra, validator

from .types import ResourceModels
from .resource import Resource

logger = logging.getLogger(__file__)

_EXISTING_RESOURCE_TYPES = {klass.TYPE_VALUE for klass in ResourceModels.__args__}


class GenericResource(Resource):
    """This class is used for all resource types that we haven't had time to implement yet"""

    ALLOW_EXISTING_TYPES: ClassVar[bool] = True
    Type: str

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
