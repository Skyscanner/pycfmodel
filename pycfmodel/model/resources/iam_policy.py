from typing import ClassVar, Optional

from ..base import CustomModel
from ..types import ResolvableStr, ResolvableStrOrList, Resolvable
from .properties.policy_document import PolicyDocument
from .resource import Resource


class IAMPolicyProperties(CustomModel):
    Groups: Optional[ResolvableStrOrList] = None
    PolicyDocument: Resolvable[PolicyDocument]
    PolicyName: ResolvableStr
    Roles: Optional[ResolvableStrOrList] = None
    Users: Optional[ResolvableStrOrList] = None


class IAMPolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::Policy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMPolicyProperties]
