from typing import ClassVar, Optional, List

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, Resolvable
from pycfmodel.model.resources.properties.policy_document import PolicyDocument


class IAMManagedPolicyProperties(CustomModel):
    Description: Optional[ResolvableStr] = None
    Groups: Optional[Resolvable[List[ResolvableStr]]] = None
    ManagedPolicyName: Optional[ResolvableStr] = None
    Path: Optional[ResolvableStr] = None
    PolicyDocument: Resolvable[PolicyDocument]
    Roles: Optional[Resolvable[List[ResolvableStr]]] = None
    Users: Optional[Resolvable[List[ResolvableStr]]] = None


class IAMManagedPolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::ManagedPolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMManagedPolicyProperties]
