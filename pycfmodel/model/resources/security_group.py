from typing import ClassVar, Optional, List, Union, Dict

from ..types import ResolvableStr, Resolvable
from ..base import CustomModel
from .properties.security_group_egress_prop import SecurityGroupEgressProp
from .properties.security_group_ingress_prop import SecurityGroupIngressProp
from .resource import Resource


class SecurityGroupProperties(CustomModel):
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
    TYPE_VALUE: ClassVar = "AWS::EC2::SecurityGroup"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SecurityGroupProperties]
