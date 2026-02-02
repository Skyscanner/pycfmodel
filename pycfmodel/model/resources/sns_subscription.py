"""
SNSSubscription resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::SNS::Subscription.
"""

from typing import Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableStr


class SNSSubscriptionProperties(CustomModel):
    """
    Properties for AWS::SNS::Subscription.

    Properties:

    - DeliveryPolicy: The delivery policy JSON assigned to the subscription. Enables the subscriber to...
    - Endpoint: The subscription's endpoint. The endpoint value depends on the protocol that you...
    - FilterPolicy: The filter policy JSON assigned to the subscription. Enables the subscriber to f...
    - FilterPolicyScope: This attribute lets you choose the filtering scope by using one of the following...
    - Protocol: The subscription's protocol.
    - RawMessageDelivery: When set to true, enables raw message delivery. Raw messages don't contain any J...
    - RedrivePolicy: When specified, sends undeliverable messages to the specified Amazon SQS dead-le...
    - Region: For cross-region subscriptions, the region in which the topic resides.If no regi...
    - ReplayPolicy: Specifies whether Amazon SNS resends the notification to the subscription when a...
    - SubscriptionRoleArn: This property applies only to Amazon Data Firehose delivery stream subscriptions...
    - TopicArn: The ARN of the topic to subscribe to.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html)
    """

    Protocol: ResolvableStr
    TopicArn: ResolvableStr
    DeliveryPolicy: Optional[Resolvable[dict]] = None
    Endpoint: Optional[ResolvableStr] = None
    FilterPolicy: Optional[Resolvable[dict]] = None
    FilterPolicyScope: Optional[ResolvableStr] = None
    RawMessageDelivery: Optional[ResolvableBool] = None
    RedrivePolicy: Optional[Resolvable[dict]] = None
    Region: Optional[ResolvableStr] = None
    ReplayPolicy: Optional[Resolvable[dict]] = None
    SubscriptionRoleArn: Optional[ResolvableStr] = None


class SNSSubscription(Resource):
    """
    Resource Type definition for AWS::SNS::Subscription

    Properties:

    - Properties: A [SNSSubscriptionProperties][pycfmodel.model.resources.sns_subscription.SNSSubscriptionProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html)
    """

    Type: Literal["AWS::SNS::Subscription"]
    Properties: Resolvable[SNSSubscriptionProperties]
