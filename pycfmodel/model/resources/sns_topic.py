"""
SNSTopic resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::SNS::Topic.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableStr


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

    ArchivePolicy: Optional[ResolvableGeneric] = None
    ContentBasedDeduplication: Optional[ResolvableBool] = None
    DataProtectionPolicy: Optional[ResolvableGeneric] = None
    DeliveryStatusLogging: Optional[Resolvable[List[ResolvableGeneric]]] = None
    DisplayName: Optional[ResolvableStr] = None
    FifoThroughputScope: Optional[ResolvableStr] = None
    FifoTopic: Optional[ResolvableBool] = None
    KmsMasterKeyId: Optional[ResolvableStr] = None
    SignatureVersion: Optional[ResolvableStr] = None
    Subscription: Optional[Resolvable[List[ResolvableGeneric]]] = None
    Tags: Optional[Resolvable[List[ResolvableGeneric]]] = None
    TopicName: Optional[ResolvableStr] = None
    TracingConfig: Optional[ResolvableStr] = None


class SNSTopic(Resource):
    """
    The ``AWS::SNS::Topic`` resource creates a topic to which notifications can be published.
  One account can create a maximum of 100,000 standard topics and 1,000 FIFO topics. For more information, see [endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/sns.html) in the *General Reference*.
   The structure of ``AUTHPARAMS`` depends on the .signature of the API request. For more information, see [Examples of the complete Signature Version 4 signing process](https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html) in the *General Reference*.

    Properties:

    - Properties: A [SNSTopicProperties][pycfmodel.model.resources.sns_topic.SNSTopicProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html)
    """

    Type: Literal["AWS::SNS::Topic"]
    Properties: Optional[Resolvable[SNSTopicProperties]] = None
