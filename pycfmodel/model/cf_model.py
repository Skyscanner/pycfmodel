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
from datetime import date
from typing import Dict, Union, ClassVar, Optional, List

from .base import CustomModel
from .intrinsic_function import resolve
from .resources.genericresource import GenericResource
from .resources.iam_group import IAMGroup
from .resources.iam_managed_policy import IAMManagedPolicy
from .resources.iam_policy import IAMPolicy
from .resources.iam_role import IAMRole
from .resources.iam_user import IAMUser
from .resources.kms_key import KMSKey
from .resources.s3_bucket_policy import S3BucketPolicy
from .resources.security_group import SecurityGroup
from .resources.security_group_egress import SecurityGroupEgress
from .resources.security_group_ingress import SecurityGroupIngress
from .resources.sns_topic_policy import SNSTopicPolicy
from .resources.sqs_queue_policy import SQSQueuePolicy
from .parameter import Parameter

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
    GenericResource,
]


class CFModel(CustomModel):
    AWSTemplateFormatVersion: date
    Description: Optional[str] = None
    Metadata: Optional[Dict[str, Dict]] = None  # TODO, check schema
    Mappings: Dict[str, Dict[str, Dict[str, str]]] = {}
    Conditions: Dict = {}
    Transform: Optional[List]
    Outputs: Dict[str, Dict[str, Union[str, Dict]]] = {}
    Resources: Dict[str, ResourceModels] = {}
    Parameters: Dict[str, Parameter] = {}
    PSEUDO_PARAMETERS: ClassVar[Dict[str, str]] = {
        # default pseudo parameters
        "AWS::AccountId": "123456789012",
        "AWS::NotificationARNs": [],
        "AWS::NoValue": "NOVALUE",
        "AWS::Partition": "aws",
        "AWS::Region": "eu-west-1",
        "AWS::StackId": "",
        "AWS::StackName": "",
        "AWS::URLSuffix": "amazonaws.com",
    }

    def resolve(self, extra_params=None) -> "CFModel":
        extra_params = {} if extra_params is None else extra_params
        extended_parameters = {
            **self.PSEUDO_PARAMETERS,
            **{
                # default parameters
                key: parameter.get_ref_value()
                for key, parameter in self.Parameters.items()
                if parameter.Default
            },
            **extra_params,
        }
        dict_value = self.dict()
        resources = dict_value.pop("Resources")
        return CFModel(
            **dict_value,
            Resources={key: resolve(value, extended_parameters, self.Mappings) for key, value in resources.items()},
        )
