from ipaddress import IPv4Network, IPv6Network
from typing import Optional
from pydantic import validator

from pycfmodel.constants import IPV4_ZERO_VALUE, IPV6_ZERO_VALUE
from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.types import (
    ResolvableIPv4Network,
    ResolvableIPv6Network,
    ResolvableStr,
    ResolvableIntOrStr,
    ResolvableInt,
)


class SecurityGroupIngressProp(Property):
    """
    An inbound rule permits instances to receive traffic from the specified IPv4 or IPv6 CIDR address range, or from the instances associated with the specified security group.

    Properties:

    - CidrIp: The IPv4 ranges.
    - CidrIpv6: The IPv6 ranges.
    - Description: The description of an egress (outbound) security group rule.
    - FromPort: The start of port range for the TCP and UDP protocols.
    - IpProtocol: The IP protocol name (tcp, udp, icmp, icmpv6) or number ([see Protocol Numbers](http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)).
    - SourcePrefixListId: The prefix list IDs for an AWS service.
    - SourceSecurityGroupId: The ID of the security group.
    - SourceSecurityGroupName: The name of the source security group.
    - SourceSecurityGroupOwnerId: The AWS account ID for the source security group.
    - ToPort: The end of port range for the TCP and UDP protocols.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html)
    """

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
        """ Returns True if `CidrIp` matches `0.0.0.0/0`, otherwise False. """
        # Remove after this is fixed https://bugs.python.org/issue38655
        if not self.CidrIp:
            return False
        return self.CidrIp == IPv4Network(IPV4_ZERO_VALUE)

    def ipv6_slash_zero(self) -> bool:
        """ Returns True if `CidrIpv6` matches `::/0`, otherwise False. """
        # Remove after this is fixed https://bugs.python.org/issue38655
        if not self.CidrIpv6:
            return False
        return self.CidrIpv6 == IPv6Network(IPV6_ZERO_VALUE)
