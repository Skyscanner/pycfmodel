from ipaddress import IPv4Network, IPv6Network
from typing import Optional
from pydantic import validator

from ....constants import IPV4_ZERO_VALUE, IPV6_ZERO_VALUE
from ...types import ResolvableStr, ResolvableInt, ResolvableIntOrStr, ResolvableIPv4Network, ResolvableIPv6Network
from .property import Property


class SecurityGroupIngressProp(Property):
    CidrIp: Optional[ResolvableIPv4Network] = None
    CidrIpv6: Optional[ResolvableIPv6Network] = None
    Description: Optional[ResolvableStr] = None
    FromPort: Optional[ResolvableInt] = None
    IpProtocol: ResolvableIntOrStr
    SourcePrefixListId: Optional[ResolvableStr] = None
    SourceSecurityGroupId: Optional[ResolvableStr] = None
    SourceSecurityGroupName: Optional[ResolvableStr] = None
    SourceSecurityGroupOwnerId: Optional[ResolvableStr] = None
    ToPort: Optional[ResolvableInt] = None

    @validator("CidrIp", pre=True)
    def set_CidrIp(cls, v):
        return IPv4Network(v, strict=False)

    @validator("CidrIpv6", pre=True)
    def set_CidrIpv6(cls, v):
        return IPv6Network(v, strict=False)

    def ipv4_slash_zero(self) -> bool:
        if not self.CidrIp:
            return False
        return self.CidrIp == IPv4Network(IPV4_ZERO_VALUE)

    def ipv6_slash_zero(self) -> bool:
        if not self.CidrIpv6:
            return False
        return self.CidrIpv6 == IPv6Network(IPV6_ZERO_VALUE)
