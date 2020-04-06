from ipaddress import IPv4Network, IPv6Network
from typing import ClassVar, Optional
from pydantic import validator

from pycfmodel.constants import IPV4_ZERO_VALUE, IPV6_ZERO_VALUE
from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import (
    ResolvableIPv4Network,
    ResolvableIPv6Network,
    ResolvableStr,
    ResolvableInt,
    ResolvableIntOrStr,
)


class SecurityGroupIngressProperties(CustomModel):
    """
    Properties:

    - CidrIp: IPv4 address range.
    - CidrIpv6: IPv6 address range.
    - Description: Description for the security group rule.
    - FromPort: Start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type number. A value of -1 indicates all ICMP/ICMPv6 types.
    - GroupId: ID of the security group.
    - GroupName: Name of the security group.
    - IpProtocol: IP protocol name.
    - SourcePrefixListId: The prefix list IDs for an AWS service.
    - SourceSecurityGroupId: ID of the security group.
    - SourceSecurityGroupName: Name of the source security group.
    - SourceSecurityGroupOwnerId: AWS account ID for the source security group.
    - ToPort: End of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code. A value of -1 indicates all ICMP/ICMPv6 codes.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html)
    """

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
    """
    Properties:

    - Properties: A [Security Group Ingress Properties][pycfmodel.model.resources.kms_key.KMSKeyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html)
    """

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
