from typing import List, Literal, Optional, Union

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.security_group_egress_prop import SecurityGroupEgressProp
from pycfmodel.model.resources.properties.security_group_ingress_prop import (
    DBSecurityGroupIngressProp,
    SecurityGroupIngressProp,
)
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr


class SecurityGroupProperties(CustomModel):
    """
    Properties:

    - GroupDescription: Description for the security group.
    - GroupName: Name of the security group.
    - SecurityGroupEgress: Outbound rules associated with the security group.
    - SecurityGroupIngress: Inbound rules associated with the security group.
    - Tags: Array of key-value pairs.
    - VpcId: ID of the VPC for the security group.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html)
    """

    GroupDescription: ResolvableStr
    GroupName: Optional[ResolvableStr] = None
    SecurityGroupEgress: Optional[
        Resolvable[Union[SecurityGroupEgressProp, List[Resolvable[SecurityGroupEgressProp]]]]
    ] = None
    SecurityGroupIngress: Optional[
        Resolvable[Union[SecurityGroupIngressProp, List[Resolvable[SecurityGroupIngressProp]]]]
    ] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VpcId: Optional[ResolvableStr] = None


class SecurityGroup(Resource):
    """
    Properties:

    - Properties: A [Security Group Properties][pycfmodel.model.resources.security_group.SecurityGroupProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html)
    """

    Type: Literal["AWS::EC2::SecurityGroup"]
    Properties: Resolvable[SecurityGroupProperties]


class RDSDBSecurityGroupProperties(CustomModel):
    """
    Properties:

    - DBSecurityGroupIngress: Inbound rules associated with the security group.
    - EC2VpcId: The identifier of an Amazon VPC. This property indicates the VPC that this DB security group belongs to.
    - GroupDescription: Description for the security group.
    - Tags: Array of key-value pairs.

    More info at [AWS Docs](https://docs.aws.amazon.com/es_es/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html)
    """

    DBSecurityGroupIngress: List[DBSecurityGroupIngressProp]
    EC2VpcId: Optional[ResolvableStr] = None
    GroupDescription: ResolvableStr
    Tags: Optional[Resolvable[List[Tag]]] = None


class RDSDBSecurityGroup(Resource):
    Type: Literal["AWS::RDS::DBSecurityGroup"]
    Properties: Resolvable[RDSDBSecurityGroupProperties]
