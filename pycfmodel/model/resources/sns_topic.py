"""
SNSTopic resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::SNS::Topic.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable
from pycfmodel.model.types import ResolvableBool
from pycfmodel.model.types import ResolvableModel
from pycfmodel.model.types import ResolvableStr


class LoggingConfig(CustomModel):
    """
    The ``LoggingConfig`` property type specifies the ``Delivery`` status logging configuration for an [AWS::SNS::Topic](https://docs.
    """

    Protocol: ResolvableStr
    FailureFeedbackRoleArn: Optional[ResolvableStr] = None
    SuccessFeedbackRoleArn: Optional[ResolvableStr] = None
    SuccessFeedbackSampleRate: Optional[ResolvableStr] = None


ResolvableLoggingConfig = ResolvableModel(LoggingConfig)


class Subscription(CustomModel):
    """
    ``Subscription`` is an embedded property that describes the subscription endpoints of an SNS topic.
    """

    Endpoint: ResolvableStr
    Protocol: ResolvableStr


ResolvableSubscription = ResolvableModel(Subscription)


# Pre-resolved list type to avoid class body name shadowing in SNSTopicProperties.
# The SNSTopicProperties class has a field named "Subscription" (default None) which shadows
# the Subscription class when Python evaluates List[Subscription] inside the class body.
_SubscriptionList = Resolvable[List[Subscription]]


class SNSTopicProperties(CustomModel):
    """
    Properties for AWS::SNS::Topic.

    Properties:

    - ArchivePolicy: The archive policy determines the number of days SNS retains messages. You can s...
    - ContentBasedDeduplication: Enables content-based deduplication for FIFO topics.
  +  By default, ``ContentB...
    - DataProtectionPolicy: The body of the policy document you want to use for this topic.
 You can only ad...
    - DeliveryStatusLogging: The ``DeliveryStatusLogging`` configuration enables you to log the delivery stat...
    - DisplayName: The display name to use for an SNS topic with SMS subscriptions. The display nam...
    - FifoThroughputScope: 
    - FifoTopic: Set to true to create a FIFO topic.
    - KmsMasterKeyId: The ID of an AWS managed customer master key (CMK) for SNS or a custom CMK. For ...
    - SignatureVersion: The signature version corresponds to the hashing algorithm used while creating t...
    - Subscription: The SNS subscriptions (endpoints) for this topic.
  If you specify the ``Subscri...
    - Tags: The list of tags to add to a new topic.
  To be able to tag a topic on creation,...
    - TopicName: The name of the topic you want to create. Topic names must include only uppercas...
    - TracingConfig: Tracing mode of an SNS topic. By default ``TracingConfig`` is set to ``PassThrou...

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html)
    """

    ArchivePolicy: Optional[Resolvable[dict]] = None
    ContentBasedDeduplication: Optional[ResolvableBool] = None
    DataProtectionPolicy: Optional[Resolvable[dict]] = None
    DeliveryStatusLogging: Optional[Resolvable[List[LoggingConfig]]] = None
    DisplayName: Optional[ResolvableStr] = None
    FifoThroughputScope: Optional[ResolvableStr] = None
    FifoTopic: Optional[ResolvableBool] = None
    KmsMasterKeyId: Optional[ResolvableStr] = None
    SignatureVersion: Optional[ResolvableStr] = None
    Subscription: Optional[_SubscriptionList] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    TopicName: Optional[ResolvableStr] = None
    TracingConfig: Optional[ResolvableStr] = None


class SNSTopic(Resource):
    """
    The ``AWS::SNS::Topic`` resource creates a topic to which notifications can be published.

    Properties:

    - Properties: A [SNSTopicProperties][pycfmodel.model.resources.sns_topic.SNSTopicProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html)
    """

    Type: Literal["AWS::SNS::Topic"]
    Properties: Resolvable[SNSTopicProperties] = SNSTopicProperties()

