from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from pycfmodel.model.resources.autoscaling_auto_scaling_group import AutoScalingAutoScalingGroup
from pycfmodel.model.resources.cloudwatch_alarm import CloudWatchAlarm
from pycfmodel.model.resources.dynamodb_table import DynamoDBTable
from pycfmodel.model.resources.ec2_vpc_endpoint_policy import EC2VpcEndpointPolicy
from pycfmodel.model.resources.elbv2_listener import ELBv2Listener
from pycfmodel.model.resources.elbv2_target_group import ELBv2TargetGroup
from pycfmodel.model.resources.es_domain import ESDomain
from pycfmodel.model.resources.iam_group import IAMGroup
from pycfmodel.model.resources.iam_instance_profile import IAMInstanceProfile
from pycfmodel.model.resources.iam_managed_policy import IAMManagedPolicy
from pycfmodel.model.resources.iam_policy import IAMPolicy
from pycfmodel.model.resources.iam_role import IAMRole
from pycfmodel.model.resources.iam_user import IAMUser
from pycfmodel.model.resources.kms_key import KMSKey
from pycfmodel.model.resources.opensearch_domain import OpenSearchDomain
from pycfmodel.model.resources.route53_record_set import Route53RecordSet
from pycfmodel.model.resources.s3_bucket import S3Bucket
from pycfmodel.model.resources.s3_bucket_policy import S3BucketPolicy
from pycfmodel.model.resources.security_group import RDSDBSecurityGroup, SecurityGroup
from pycfmodel.model.resources.security_group_egress import SecurityGroupEgress
from pycfmodel.model.resources.security_group_ingress import RDSDBSecurityGroupIngress, SecurityGroupIngress
from pycfmodel.model.resources.sns_subscription import SNSSubscription
from pycfmodel.model.resources.sns_topic import SNSTopic
from pycfmodel.model.resources.sns_topic_policy import SNSTopicPolicy
from pycfmodel.model.resources.sqs_queue import SQSQueue
from pycfmodel.model.resources.sqs_queue_policy import SQSQueuePolicy
from pycfmodel.model.resources.wafv2_ip_set import WAFv2IPSet

ResourceModels = Annotated[
    Union[
        AutoScalingAutoScalingGroup,
        CloudWatchAlarm,
        DynamoDBTable,
        EC2VpcEndpointPolicy,
        ELBv2Listener,
        ELBv2TargetGroup,
        ESDomain,
        IAMGroup,
        IAMInstanceProfile,
        IAMManagedPolicy,
        IAMPolicy,
        IAMRole,
        IAMUser,
        KMSKey,
        OpenSearchDomain,
        RDSDBSecurityGroup,
        RDSDBSecurityGroupIngress,
        Route53RecordSet,
        S3Bucket,
        S3BucketPolicy,
        SecurityGroup,
        SecurityGroupEgress,
        SecurityGroupIngress,
        SNSSubscription,
        SNSTopic,
        SNSTopicPolicy,
        SQSQueue,
        SQSQueuePolicy,
        WAFv2IPSet,
    ],
    Field(discriminator="Type"),
]
