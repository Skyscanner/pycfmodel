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
from typing import Optional, Union, Dict

from pycfmodel.model.types import ResolvableStr
from .property import Property


class SecurityGroupEgressProp(Property):
    CidrIp: Optional[ResolvableStr]
    CidrIpv6: Optional[ResolvableStr]
    Description: Optional[ResolvableStr]
    DestinationPrefixListId: Optional[ResolvableStr]
    DestinationSecurityGroupId: Optional[ResolvableStr]
    FromPort: Optional[Union[int, Dict]]
    IpProtocol: Union[int, str, Dict]
    ToPort: Optional[Union[int, Dict]]

    def ipv4_slash_zero(self) -> bool:
        if not self.CidrIp or not isinstance(self.CidrIp, str):
            return False
        return self.CidrIp.endswith("/0")

    def ipv6_slash_zero(self) -> bool:
        if not self.CidrIpv6 or not isinstance(self.CidrIpv6, str):
            return False
        return self.CidrIpv6.endswith("/0")
