"""
Copyright 2018 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from .resources.generic_resource import GenericResource
from .resources.iam_group import IAMGroup
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


class ResourceFactory(object):
    resource_classes = {
        "AWS::IAM::Policy": IAMPolicy,
        "AWS::IAM::Role": IAMRole,
        "AWS::S3::BucketPolicy": S3BucketPolicy,
        "AWS::IAM::ManagedPolicy": IAMManagedPolicy,
        "AWS::IAM::Group": IAMGroup,
        "AWS::EC2::SecurityGroup": SecurityGroup,
        "AWS::EC2::SecurityGroupEgress": SecurityGroupEgress,
        "AWS::EC2::SecurityGroupIngress": SecurityGroupIngress,
        "AWS::SQS::QueuePolicy": SQSQueuePolicy,
        "AWS::SNS::TopicPolicy": SNSTopicPolicy,
        "AWS::KMS::Key": KMSKey,
    }

    def create_resource(self, logical_id, value):
        resource = self.resource_classes.get(
            value.get("Type"),
            GenericResource,
        )
        return resource(logical_id, value)
