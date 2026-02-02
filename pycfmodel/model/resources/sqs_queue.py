"""
SQSQueue resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::SQS::Queue.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable
from pycfmodel.model.types import ResolvableBool
from pycfmodel.model.types import ResolvableInt
from pycfmodel.model.types import ResolvableModel
from pycfmodel.model.types import ResolvableStr


class Tag(CustomModel):
    """
    
    """

    Key: ResolvableStr
    Value: ResolvableStr


ResolvableTag = ResolvableModel(Tag)


class SQSQueueProperties(CustomModel):
    """
    Properties for AWS::SQS::Queue.

    Properties:

    - ContentBasedDeduplication: For first-in-first-out (FIFO) queues, specifies whether to enable content-based ...
    - DeduplicationScope: For high throughput for FIFO queues, specifies whether message deduplication occ...
    - DelaySeconds: The time in seconds for which the delivery of all messages in the queue is delay...
    - FifoQueue: If set to true, creates a FIFO queue. If you don't specify this property, SQS cr...
    - FifoThroughputLimit: For high throughput for FIFO queues, specifies whether the FIFO queue throughput...
    - KmsDataKeyReusePeriodSeconds: The length of time in seconds for which SQS can reuse a data key to encrypt or d...
    - KmsMasterKeyId: The ID of an AWS Key Management Service (KMS) for SQS, or a custom KMS. To use t...
    - MaximumMessageSize: The limit of how many bytes that a message can contain before SQS rejects it. Yo...
    - MessageRetentionPeriod: The number of seconds that SQS retains a message. You can specify an integer val...
    - QueueName: A name for the queue. To create a FIFO queue, the name of your FIFO queue must e...
    - ReceiveMessageWaitTimeSeconds: Specifies the duration, in seconds, that the ReceiveMessage action call waits un...
    - RedriveAllowPolicy: The string that includes the parameters for the permissions for the dead-letter ...
    - RedrivePolicy: The string that includes the parameters for the dead-letter queue functionality ...
    - SqsManagedSseEnabled: Enables server-side queue encryption using SQS owned encryption keys. Only one s...
    - Tags: The tags that you attach to this queue. For more information, see [Resource tag]...
    - VisibilityTimeout: The length of time during which a message will be unavailable after a message is...

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html)
    """

    ContentBasedDeduplication: Optional[ResolvableBool] = None
    DeduplicationScope: Optional[ResolvableStr] = None
    DelaySeconds: Optional[ResolvableInt] = None
    FifoQueue: Optional[ResolvableBool] = None
    FifoThroughputLimit: Optional[ResolvableStr] = None
    KmsDataKeyReusePeriodSeconds: Optional[ResolvableInt] = None
    KmsMasterKeyId: Optional[ResolvableStr] = None
    MaximumMessageSize: Optional[ResolvableInt] = None
    MessageRetentionPeriod: Optional[ResolvableInt] = None
    QueueName: Optional[ResolvableStr] = None
    ReceiveMessageWaitTimeSeconds: Optional[ResolvableInt] = None
    RedriveAllowPolicy: Optional[ResolvableGeneric] = None
    RedrivePolicy: Optional[ResolvableGeneric] = None
    SqsManagedSseEnabled: Optional[ResolvableBool] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VisibilityTimeout: Optional[ResolvableInt] = None


class SQSQueue(Resource):
    """
    The ``AWS::SQS::Queue`` resource creates an SQS standard or FIFO queue.

    Properties:

    - Properties: A [SQSQueueProperties][pycfmodel.model.resources.sqs_queue.SQSQueueProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html)
    """

    Type: Literal["AWS::SQS::Queue"]
    Properties: Optional[Resolvable[SQSQueueProperties]] = None
