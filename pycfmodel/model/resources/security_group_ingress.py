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
from typing import ClassVar, Optional

from ..types import ResolvableStr, ResolvableIntOrStr, ResolvableInt
from ..base import CustomModel
from .resource import Resource


class SecurityGroupIngressProperties(CustomModel):
    CidrIp: Optional[ResolvableStr]
    CidrIpv6: Optional[ResolvableStr]
    Description: Optional[ResolvableStr]
    FromPort: Optional[ResolvableInt]
    GroupId: Optional[ResolvableStr]
    GroupName: Optional[ResolvableStr]
    IpProtocol: ResolvableIntOrStr
    SourcePrefixListId: Optional[ResolvableStr]
    SourceSecurityGroupId: Optional[ResolvableStr]
    SourceSecurityGroupName: Optional[ResolvableStr]
    SourceSecurityGroupOwnerId: Optional[ResolvableStr]
    ToPort: Optional[ResolvableInt]


class SecurityGroupIngress(Resource):
    TYPE_VALUE: ClassVar = "AWS::EC2::SecurityGroupIngress"
    Type: str = TYPE_VALUE
    Properties: SecurityGroupIngressProperties

    def ipv4_slash_zero(self) -> bool:
        if not self.Properties.CidrIp or not isinstance(self.Properties.CidrIp, str):
            return False
        return self.Properties.CidrIp.endswith("/0")

    def ipv6_slash_zero(self) -> bool:
        if not self.Properties.CidrIpv6 or not isinstance(self.Properties.CidrIpv6, str):
            return False
        return self.Properties.CidrIpv6.endswith("/0")
