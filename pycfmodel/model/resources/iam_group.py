from typing import ClassVar, List, Optional

from ..base import CustomModel
from ..types import ResolvableStr, Resolvable
from .resource import Resource
from .iam_policy import IAMPolicy


class IAMGroupProperties(CustomModel):
    GroupName: Optional[ResolvableStr] = None
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    Path: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[IAMPolicy]]] = None


class IAMGroup(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::Group"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMGroupProperties]
