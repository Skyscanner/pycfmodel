from typing import ClassVar, List, Optional

from ..types import ResolvableStr, ResolvableIntOrStr, Resolvable
from ..base import CustomModel
from .resource import Resource
from .properties.policy import Policy
from .properties.policy_document import PolicyDocument


class IAMRoleProperties(CustomModel):
    AssumeRolePolicyDocument: Resolvable[PolicyDocument]
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    MaxSessionDuration: Optional[ResolvableIntOrStr] = None
    Path: Optional[ResolvableStr] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[Resolvable[Policy]]]] = None
    RoleName: Optional[ResolvableStr] = None


class IAMRole(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::Role"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMRoleProperties]
