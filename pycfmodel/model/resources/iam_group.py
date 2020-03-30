from typing import ClassVar, List, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.iam_policy import IAMPolicy
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, Resolvable


class IAMGroupProperties(CustomModel):
    GroupName: Optional[ResolvableStr] = None
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    Path: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[IAMPolicy]]] = None


class IAMGroup(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::Group"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMGroupProperties]
