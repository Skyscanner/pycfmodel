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
from typing import Dict, ClassVar, Optional

from pydantic import validator

from ...model.types import ResolvableStrOrList, ResolvableStr, ResolvableCondition
from ..base import CustomModel
from ..parameter import Parameter


class Resource(CustomModel):
    TYPE_VALUE: ClassVar[str]
    Type: str
    Condition: Optional[ResolvableCondition] = None
    CreatePolicy: Optional[Dict] = None
    DeletionPolicy: Optional[ResolvableStr] = None
    DependsOn: Optional[ResolvableStrOrList] = None
    Metadata: Optional[Dict] = None
    UpdatePolicy: Optional[Dict] = None
    UpdateReplacePolicy: Optional[ResolvableStr] = None

    @validator("Type")
    def check_type(cls, value):
        if value != cls.TYPE_VALUE:
            raise ValueError(f"Value needs to be {cls.TYPE_VALUE}")
        return value

    def has_hardcoded_credentials(self) -> bool:
        if not self.Metadata or not self.Metadata.get("AWS::CloudFormation::Authentication"):
            return False

        for auth in self.Metadata["AWS::CloudFormation::Authentication"].values():
            if not all(
                [
                    auth.get("accessKeyId", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("password", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("secretKey", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                ]
            ):
                return True

        return False
