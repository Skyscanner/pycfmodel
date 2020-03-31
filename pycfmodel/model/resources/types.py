from typing import Union

from pycfmodel.model.resources.iam_group import IAMGroup
from pycfmodel.model.resources.iam_managed_policy import IAMManagedPolicy
from pycfmodel.model.resources.iam_policy import IAMPolicy
from pycfmodel.model.resources.iam_role import IAMRole
from pycfmodel.model.resources.iam_user import IAMUser
from pycfmodel.model.resources.kms_key import KMSKey
from pycfmodel.model.resources.s3_bucket_policy import S3BucketPolicy
from pycfmodel.model.resources.security_group import SecurityGroup
from pycfmodel.model.resources.security_group_egress import SecurityGroupEgress
from pycfmodel.model.resources.security_group_ingress import SecurityGroupIngress
from pycfmodel.model.resources.sns_topic_policy import SNSTopicPolicy
from pycfmodel.model.resources.sqs_queue_policy import SQSQueuePolicy

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
