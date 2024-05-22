from typing import Literal, Optional

from pycfmodel.model.resources.properties.security_group_ingress_prop import (
    DBSecurityGroupIngressResourceProp,
    SecurityGroupIngressProp,
)
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr


class SecurityGroupIngressProperties(SecurityGroupIngressProp):
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

    GroupId: Optional[ResolvableStr] = None
    GroupName: Optional[ResolvableStr] = None


class SecurityGroupIngress(Resource):
    """
    Properties:

    - Properties: A [Security Group Ingress Properties][pycfmodel.model.resources.kms_key.KMSKeyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html)
    """

    Type: Literal["AWS::EC2::SecurityGroupIngress"]
    Properties: SecurityGroupIngressProperties

    def ipv4_slash_zero(self) -> bool:
        return self.Properties.ipv4_slash_zero()

    def ipv6_slash_zero(self) -> bool:
        return self.Properties.ipv6_slash_zero()


class RDSDBSecurityGroupIngress(Resource):
    Type: Literal["AWS::RDS::DBSecurityGroupIngress"]
    Properties: DBSecurityGroupIngressResourceProp
