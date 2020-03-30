from ipaddress import IPv4Network, IPv6Network
from typing import ClassVar, Optional
from pydantic import validator

from ...constants import IPV4_ZERO_VALUE, IPV6_ZERO_VALUE
from ..types import ResolvableStr, ResolvableIntOrStr, ResolvableInt, ResolvableIPv4Network, ResolvableIPv6Network
from ..base import CustomModel
from .resource import Resource


class SecurityGroupIngressProperties(CustomModel):
    CidrIp: Optional[ResolvableIPv4Network] = None
    CidrIpv6: Optional[ResolvableIPv6Network] = None
    Description: Optional[ResolvableStr] = None
    FromPort: Optional[ResolvableInt] = None
    GroupId: Optional[ResolvableStr] = None
    GroupName: Optional[ResolvableStr] = None
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


class SecurityGroupIngress(Resource):
    TYPE_VALUE: ClassVar = "AWS::EC2::SecurityGroupIngress"
    Type: str = TYPE_VALUE
    Properties: SecurityGroupIngressProperties

    def ipv4_slash_zero(self) -> bool:
        if not self.Properties.CidrIp:
            return False
        return self.Properties.CidrIp == IPv4Network(IPV4_ZERO_VALUE)

    def ipv6_slash_zero(self) -> bool:
        if not self.Properties.CidrIpv6:
            return False
        return self.Properties.CidrIpv6 == IPv6Network(IPV6_ZERO_VALUE)
