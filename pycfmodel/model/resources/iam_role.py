from typing import ClassVar, List, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr, ResolvableIntOrStr


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
