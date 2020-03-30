from typing import ClassVar, Optional, List

from ..base import CustomModel
from ..types import ResolvableStr, Resolvable
from .resource import Resource
from .properties.policy_document import PolicyDocument


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
