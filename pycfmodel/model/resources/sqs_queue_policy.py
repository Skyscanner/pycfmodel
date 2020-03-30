from typing import ClassVar, List

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr


class SQSQueuePolicyProperties(CustomModel):
    PolicyDocument: Resolvable[PolicyDocument]
    Queues: Resolvable[List[ResolvableStr]]


class SQSQueuePolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::SQS::QueuePolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SQSQueuePolicyProperties]
