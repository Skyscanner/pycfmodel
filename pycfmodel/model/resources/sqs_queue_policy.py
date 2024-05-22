from typing import List, Literal

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


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

    Type: Literal["AWS::SQS::QueuePolicy"]
    Properties: Resolvable[SQSQueuePolicyProperties]

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        return [OptionallyNamedPolicyDocument(name=None, policy_document=self.Properties.PolicyDocument)]
