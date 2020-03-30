from typing import ClassVar, Optional, List, Union, Dict

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.security_group_egress_prop import SecurityGroupEgressProp
from pycfmodel.model.resources.properties.security_group_ingress_prop import SecurityGroupIngressProp
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, Resolvable


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
