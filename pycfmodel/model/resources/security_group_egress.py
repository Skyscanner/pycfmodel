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
from ipaddress import IPv4Network, IPv6Network
from typing import ClassVar, Optional
from pydantic import validator

from ...constants import IPV4_ZERO_VALUE, IPV6_ZERO_VALUE
from ..types import ResolvableStr, ResolvableInt, ResolvableIntOrStr, ResolvableIPv4Network, ResolvableIPv6Network
from ..base import CustomModel
from .resource import Resource


class SecurityGroupEgressProperties(CustomModel):
    CidrIp: Optional[ResolvableIPv4Network] = None
    CidrIpv6: Optional[ResolvableIPv6Network] = None
    Description: Optional[ResolvableStr] = None
    DestinationPrefixListId: Optional[ResolvableStr] = None
    DestinationSecurityGroupId: Optional[ResolvableStr] = None
    FromPort: Optional[ResolvableInt] = None
    GroupId: Optional[ResolvableStr] = None
    IpProtocol: ResolvableIntOrStr
    ToPort: Optional[ResolvableInt] = None

    @validator("CidrIp", pre=True)
    def set_CidrIp(cls, v):
        return IPv4Network(v, strict=False)

    @validator("CidrIpv6", pre=True)
    def set_CidrIpv6(cls, v):
        return IPv6Network(v, strict=False)


class SecurityGroupEgress(Resource):
    TYPE_VALUE: ClassVar = "AWS::EC2::SecurityGroupEgress"
    Type: str = TYPE_VALUE
    Properties: SecurityGroupEgressProperties

    def ipv4_slash_zero(self) -> bool:
        if not self.Properties.CidrIp:
            return False
        return self.Properties.CidrIp == IPv4Network(IPV4_ZERO_VALUE)

    def ipv6_slash_zero(self) -> bool:
        if not self.Properties.CidrIpv6:
            return False
        return self.Properties.CidrIpv6 == IPv6Network(IPV6_ZERO_VALUE)
