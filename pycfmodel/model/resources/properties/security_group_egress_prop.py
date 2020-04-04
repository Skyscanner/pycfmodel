from ipaddress import IPv4Network, IPv6Network
from typing import Optional
from pydantic import validator

from pycfmodel.constants import IPV4_ZERO_VALUE, IPV6_ZERO_VALUE
from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.types import (
    ResolvableIPv4Network,
    ResolvableIPv6Network,
    ResolvableStr,
    ResolvableInt,
    ResolvableIntOrStr,
)


class SecurityGroupEgressProp(Property):
    """
    An outbound rule permits instances to send traffic from the specified IPv4 or IPv6 CIDR address range, or to the instances associated with the specified security group.

    Properties:

    - CidrIp: The IPv4 ranges.
    - CidrIpv6: The IPv6 ranges.
    - Description: The description of an egress (outbound) security group rule.
    - DestinationPrefixListId: The prefix list IDs for an AWS service.
    - DestinationSecurityGroupId: The ID of the security group.
    - FromPort: The start of port range for the TCP and UDP protocols.
    - IpProtocol: The IP protocol name (tcp, udp, icmp, icmpv6) or number ([see Protocol Numbers](http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)).
    - ToPort: The end of port range for the TCP and UDP protocols.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html)
    """

    CidrIp: Optional[ResolvableIPv4Network] = None
    CidrIpv6: Optional[ResolvableIPv6Network] = None
    Description: Optional[ResolvableStr] = None
    DestinationPrefixListId: Optional[ResolvableStr] = None
    DestinationSecurityGroupId: Optional[ResolvableStr] = None
    FromPort: Optional[ResolvableInt] = None
    IpProtocol: ResolvableIntOrStr
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
