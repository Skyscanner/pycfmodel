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
from typing import ClassVar, List, Optional, Dict

from .iam_managed_policy import IAMManagedPolicy
from ..parameter import Parameter
from ..types import ResolvableStr, Resolvable
from ..base import CustomModel
from .properties.policy import Policy
from .resource import Resource
from ...constants import REGEX_AWS_MANAGED_ARN


class IAMUserProperties(CustomModel):
    Groups: Optional[Resolvable[List[ResolvableStr]]] = None
    LoginProfile: Optional[Dict] = None
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    Path: Optional[ResolvableStr] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[Resolvable[Policy]]]] = None
    UserName: Optional[ResolvableStr] = None

    @property
    def ManagedPolicies(self) -> List[IAMManagedPolicy]:
        return [
            IAMManagedPolicy.from_arn(managed_policy_arn)
            for managed_policy_arn in self.ManagedPolicyArns
            if REGEX_AWS_MANAGED_ARN.match(managed_policy_arn)
        ]


class IAMUser(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::User"
    Type: str = TYPE_VALUE
    Properties: Optional[Resolvable[IAMUserProperties]]

    def has_hardcoded_credentials(self) -> bool:
        if self.Properties:
            login_profile = self.Properties.LoginProfile
            if login_profile and login_profile.get("Password"):
                if login_profile["Password"] != Parameter.NO_ECHO_NO_DEFAULT:
                    return True

        return super().has_hardcoded_credentials()
