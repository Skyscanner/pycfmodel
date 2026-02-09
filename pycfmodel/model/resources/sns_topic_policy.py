from typing import List, Literal

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


class SNSTopicPolicyProperties(CustomModel):
    """
    Properties:

    - PolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - Topics: ARNs of the topics to add the policy.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html)
    """

    PolicyDocument: Resolvable[PolicyDocument]
    Topics: List[ResolvableStr]


class SNSTopicPolicy(Resource):
    """
    Properties:

    - Properties: A [SNS Topic Policy][pycfmodel.model.resources.sns_topic_policy.SNSTopicPolicyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html)
    """

    Type: Literal["AWS::SNS::TopicPolicy"]
    Properties: Resolvable[SNSTopicPolicyProperties]

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        return [OptionallyNamedPolicyDocument(name=None, policy_document=self.Properties.PolicyDocument)]
