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
from typing import Optional

from ...types import ResolvableStr, ResolvableInt, ResolvableIntOrStr
from .property import Property


class SecurityGroupEgressProp(Property):
    CidrIp: Optional[ResolvableStr] = None
    CidrIpv6: Optional[ResolvableStr] = None
    Description: Optional[ResolvableStr] = None
    DestinationPrefixListId: Optional[ResolvableStr] = None
    DestinationSecurityGroupId: Optional[ResolvableStr] = None
    FromPort: Optional[ResolvableInt] = None
    IpProtocol: ResolvableIntOrStr
    ToPort: Optional[ResolvableInt] = None

    def ipv4_slash_zero(self) -> bool:
        if not self.CidrIp or not isinstance(self.CidrIp, str):
            return False
        return self.CidrIp.endswith("/0")

    def ipv6_slash_zero(self) -> bool:
        if not self.CidrIpv6 or not isinstance(self.CidrIpv6, str):
            return False
        return self.CidrIpv6.endswith("/0")

    def ipv4_private_addr(self) -> bool:
        # follows https://tools.ietf.org/html/rfc1918
        if not self.CidrIp or not isinstance(self.CidrIp, str):
            return False
        private_blocks = set({"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"})
        return self.CidrIp in private_blocks

    def ipv6_private_addr(self) -> bool:
        # follows https://tools.ietf.org/html/rfc4193
        if not self.CidrIpv6 or not isinstance(self.CidrIpv6, str):
            return False
        return self.CidrIpv6.lower().startswith("fc") or self.CidrIpv6.lower().startswith("fd")
