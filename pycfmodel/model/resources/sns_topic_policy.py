from typing import ClassVar, List

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr


class SNSTopicPolicyProperties(CustomModel):
    PolicyDocument: Resolvable[PolicyDocument]
    Topics: List[ResolvableStr]


class SNSTopicPolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::SNS::TopicPolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SNSTopicPolicyProperties]
