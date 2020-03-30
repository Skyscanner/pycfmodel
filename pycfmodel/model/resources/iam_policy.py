from typing import ClassVar, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.types import ResolvableStrOrList, ResolvableStr, Resolvable


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
