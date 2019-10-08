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
from typing import ClassVar, Optional, List

from ..base import CustomModel
from ..types import ResolvableStr
from .resource import Resource
from .properties.policy_document import PolicyDocument


class IAMPolicyProperties(CustomModel):
    Groups: Optional[List[ResolvableStr]] = None
    PolicyDocument: PolicyDocument
    PolicyName: ResolvableStr
    Roles: Optional[List[ResolvableStr]] = None
    Users: Optional[List[ResolvableStr]] = None


class IAMPolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::Policy"
    Type: str = TYPE_VALUE
    Properties: IAMPolicyProperties
