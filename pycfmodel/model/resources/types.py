from typing import Union

from .iam_group import IAMGroup
from .iam_managed_policy import IAMManagedPolicy
from .iam_policy import IAMPolicy
from .iam_role import IAMRole
from .iam_user import IAMUser
from .kms_key import KMSKey
from .s3_bucket_policy import S3BucketPolicy
from .security_group import SecurityGroup
from .security_group_egress import SecurityGroupEgress
from .security_group_ingress import SecurityGroupIngress
from .sns_topic_policy import SNSTopicPolicy
from .sqs_queue_policy import SQSQueuePolicy


ResourceModels = Union[
    IAMGroup,
    IAMManagedPolicy,
    IAMPolicy,
    IAMRole,
    IAMUser,
    KMSKey,
    S3BucketPolicy,
    SecurityGroup,
    SecurityGroupEgress,
    SecurityGroupIngress,
    SNSTopicPolicy,
    SQSQueuePolicy,
]
