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
from typing import Union

from ..types import Resolvable
from .properties.policy import Policy
from .properties.policy_document import PolicyDocument
from .properties.security_group_egress_prop import SecurityGroupEgressProp
from .properties.security_group_ingress_prop import SecurityGroupIngressProp
from .properties.statement import Statement
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


ResolvablePolicy = Resolvable[Policy]
ResolvablePolicyDocument = Resolvable[PolicyDocument]
ResolvableSecurityGroupEgressProp = Resolvable[SecurityGroupEgressProp]
ResolvableSecurityGroupIngressProp = Resolvable[SecurityGroupIngressProp]
ResolvableStatement = Resolvable[Statement]
ResolvableIAMPolicy = Resolvable[IAMPolicy]

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
