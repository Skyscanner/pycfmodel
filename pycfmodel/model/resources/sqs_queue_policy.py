from typing import ClassVar, List

from ..types import ResolvableStr, Resolvable
from ..base import CustomModel
from .resource import Resource
from .properties.policy_document import PolicyDocument


class SQSQueuePolicyProperties(CustomModel):
    PolicyDocument: Resolvable[PolicyDocument]
    Queues: Resolvable[List[ResolvableStr]]


class SQSQueuePolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::SQS::QueuePolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SQSQueuePolicyProperties]
