"""
Copyright 2018-2019 Skyscanner Ltd

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

from ..base import CustomModel
from .properties.policy import Policy
from ..parameter import Parameter


class Resource(CustomModel):
    TYPE_VALUE: ClassVar[str]
    Type: str
    Metadata: Optional[Dict] = None

    @validator("Type")
    def check_type(cls, value):
        if value != cls.TYPE_VALUE:
            raise ValueError(f"Value needs to be {cls.TYPE_VALUE}")
        return value

    def get_policies(self, policies):
        if not policies:
            return []

        new_policies = []
        for p in policies:

            # TODO: Wait to resolve to be implemented
            if "Fn::If" in p:
                if_policies = p["Fn::If"]
                new_policies.append(Policy(if_policies[1]))
                new_policies.append(Policy(if_policies[2]))
            else:
                new_policies.append(Policy(p))
        return new_policies

    def get_managed_policy_arns(self, arns):
        if not arns:
            return []

        # TODO: Use resolver // Implement boto3 client to download managed policies
        if isinstance(arns, dict) and "Fn::If" in arns:
            return arns["Fn::If"][1] + arns["Fn::If"][2]
        elif isinstance(arns, list):
            return arns

        return []

    def has_hardcoded_credentials(self):
        if not self.Metadata or not self.Metadata.get("AWS::CloudFormation::Authentication"):
            return False

        for auth_name, auth in self.Metadata.get("AWS::CloudFormation::Authentication", {}).items():
            return not all(
                [
                    auth.get("accessKeyId", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("password", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("secretKey", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                ]
            )
