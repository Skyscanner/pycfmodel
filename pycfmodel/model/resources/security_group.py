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
from typing import ClassVar, Optional, List, Union

from ..types import ResolvableStr, Resolvable
from ..base import CustomModel
from .properties.security_group_egress_prop import SecurityGroupEgressProp
from .properties.security_group_ingress_prop import SecurityGroupIngressProp
from .resource import Resource


class SecurityGroupProperties(CustomModel):
    GroupDescription: ResolvableStr
    GroupName: Optional[ResolvableStr]
    SecurityGroupEgress: Optional[Resolvable[Union[SecurityGroupEgressProp, List[Resolvable[SecurityGroupEgressProp]]]]]
    SecurityGroupIngress: Optional[
        Resolvable[Union[SecurityGroupIngressProp, List[Resolvable[SecurityGroupIngressProp]]]]
    ]
    Tags: Optional[List]
    VpcId: Optional[ResolvableStr]


class SecurityGroup(Resource):
    TYPE_VALUE: ClassVar = "AWS::EC2::SecurityGroup"
    Type: str = TYPE_VALUE
    Properties: SecurityGroupProperties
