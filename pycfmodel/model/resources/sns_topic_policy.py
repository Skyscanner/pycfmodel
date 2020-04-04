from typing import ClassVar, List

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr


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

    TYPE_VALUE: ClassVar = "AWS::SNS::TopicPolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[SNSTopicPolicyProperties]
