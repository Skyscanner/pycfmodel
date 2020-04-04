from typing import ClassVar, List

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr


class SQSQueuePolicyProperties(CustomModel):
    """
    Properties:

    - PolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - Queues: URLs of the queues to add the policy.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html)
    """

    PolicyDocument: Resolvable[PolicyDocument]
    Queues: Resolvable[List[ResolvableStr]]


class SQSQueuePolicy(Resource):
    """
    Properties:

    - Properties: A [SQS Queue Policy Properties][pycfmodel.model.resources.sqs_queue_policy.SQSQueuePolicy] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html)
    """

    TYPE_VALUE: ClassVar = "AWS::SQS::QueuePolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SQSQueuePolicyProperties]
