"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import Any, Dict

from .resources.resource import Resource
from .resources.iam_group import IAMGroup
from .resources.iam_user import IAMUser
from .resources.iam_managed_policy import IAMManagedPolicy
from .resources.iam_policy import IAMPolicy
from .resources.iam_role import IAMRole
from .resources.s3_bucket_policy import S3BucketPolicy
from .resources.security_group import SecurityGroup
from .resources.security_group_egress import SecurityGroupEgress
from .resources.security_group_ingress import SecurityGroupIngress
from .resources.sqs_queue_policy import SQSQueuePolicy
from .resources.sns_topic_policy import SNSTopicPolicy
from .resources.kms_key import KMSKey


_RESOURCE_MAP = {
    "AWS::EC2::SecurityGroup": SecurityGroup,
    "AWS::EC2::SecurityGroupEgress": SecurityGroupEgress,
    "AWS::EC2::SecurityGroupIngress": SecurityGroupIngress,
    "AWS::IAM::Group": IAMGroup,
    "AWS::IAM::ManagedPolicy": IAMManagedPolicy,
    "AWS::IAM::Policy": IAMPolicy,
    "AWS::IAM::Role": IAMRole,
    "AWS::IAM::User": IAMUser,
    "AWS::KMS::Key": KMSKey,
    "AWS::S3::BucketPolicy": S3BucketPolicy,
    "AWS::SNS::TopicPolicy": SNSTopicPolicy,
    "AWS::SQS::QueuePolicy": SQSQueuePolicy,
}
_DEFAULT_RESOURCE = Resource


def create_resource(logical_id: str, value: Dict[str, Any]) -> Resource:
    resource = _RESOURCE_MAP.get(value.get("Type"), _DEFAULT_RESOURCE)
    return resource(logical_id, value)
