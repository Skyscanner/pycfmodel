from typing import ClassVar, List

from ..types import ResolvableStr, Resolvable
from ..base import CustomModel
from .resource import Resource
from .properties.policy_document import PolicyDocument


class SNSTopicPolicyProperties(CustomModel):
    PolicyDocument: Resolvable[PolicyDocument]
    Topics: List[ResolvableStr]


class SNSTopicPolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::SNS::TopicPolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SNSTopicPolicyProperties]
