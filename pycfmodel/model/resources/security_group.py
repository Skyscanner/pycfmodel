from typing import ClassVar, Optional, List, Union, Dict

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.security_group_egress_prop import SecurityGroupEgressProp
from pycfmodel.model.resources.properties.security_group_ingress_prop import SecurityGroupIngressProp
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, Resolvable


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
    Tags: Optional[Resolvable[List[Dict]]] = None
    VpcId: Optional[ResolvableStr] = None


class SecurityGroup(Resource):
    """
    Properties:

    - Properties: A [Security Group Properties][pycfmodel.model.resources.security_group.SecurityGroupProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html)
    """

    TYPE_VALUE: ClassVar = "AWS::EC2::SecurityGroup"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SecurityGroupProperties]
