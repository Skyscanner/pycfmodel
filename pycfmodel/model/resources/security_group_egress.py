from typing import Literal, Optional

from pycfmodel.model.resources.properties.security_group_egress_prop import SecurityGroupEgressProp
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr


class SecurityGroupEgressProperties(SecurityGroupEgressProp):
    """
    Properties:

    - CidrIp: IPv4 address range.
    - CidrIpv6: IPv6 address range.
    - Description: Description for the security group rule.
    - DestinationPrefixListId: The prefix list IDs for an AWS service.
    - DestinationSecurityGroupId: ID of the destination VPC security group.
    - FromPort: Start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type number. A value of -1 indicates all ICMP/ICMPv6 types.
    - GroupId: ID of the security group.
    - IpProtocol: IP protocol name.
    - ToPort: End of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code. A value of -1 indicates all ICMP/ICMPv6 codes.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html)
    """

    GroupId: Optional[ResolvableStr] = None


class SecurityGroupEgress(Resource):
    """
    Properties:

    - Properties: A [Security Group Egress Properties][pycfmodel.model.resources.security_group_egress.SecurityGroupEgressProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html)
    """

    Type: Literal["AWS::EC2::SecurityGroupEgress"]
    Properties: SecurityGroupEgressProperties

    def ipv4_slash_zero(self) -> bool:
        return self.Properties.ipv4_slash_zero()

    def ipv6_slash_zero(self) -> bool:
        return self.Properties.ipv6_slash_zero()
