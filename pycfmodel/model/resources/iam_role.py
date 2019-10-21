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
from typing import ClassVar, List, Optional

from ..types import ResolvableStr, ResolvableIntOrStr
from ..base import CustomModel
from .resource import Resource
from .types import ResolvablePolicy, ResolvablePolicyDocument


class IAMRoleProperties(CustomModel):
    AssumeRolePolicyDocument: ResolvablePolicyDocument
    ManagedPolicyArns: Optional[List[ResolvableStr]] = None
    MaxSessionDuration: Optional[ResolvableIntOrStr] = None
    Path: Optional[ResolvableStr] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[List[ResolvablePolicy]] = None
    RoleName: Optional[ResolvableStr] = None


class IAMRole(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::Role"
    Type: str = TYPE_VALUE
    Properties: IAMRoleProperties
