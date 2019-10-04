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
from typing import ClassVar, List, Optional, Dict

from ..types import ResolvableStr
from ..base import CustomModel
from .iam_policy import IAMPolicy
from .resource import Resource


class IAMUserProperties(CustomModel):
    Groups: Optional[List[ResolvableStr]] = None
    LoginProfile: Optional[Dict] = None
    ManagedPolicyArns: Optional[List[ResolvableStr]] = None
    Path: Optional[str] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[List[IAMPolicy]] = None
    UserName: Optional[ResolvableStr] = None


class IAMUser(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::User"
    Type: str = TYPE_VALUE
    Properties: IAMUserProperties
