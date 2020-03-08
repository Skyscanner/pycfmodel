"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import pytest

from pycfmodel.constants import AWS_IAM_MANAGED_POLICIES_PATH
from pycfmodel.model.resources.iam_managed_policy import IAMManagedPolicy, IAMManagedPolicyNotFoundException


@pytest.mark.parametrize(
    "partial_arn",
    [
        file.relative_to(AWS_IAM_MANAGED_POLICIES_PATH).with_suffix("")
        for file in AWS_IAM_MANAGED_POLICIES_PATH.rglob("*.json")
    ],
)
def test_all_aws_managed_policy(partial_arn):
    aws_managed_policy_arn = f"arn:aws:iam::aws:policy/{partial_arn}"
    aws_managed_policy = IAMManagedPolicy.from_arn(aws_managed_policy_arn)
    assert isinstance(aws_managed_policy, IAMManagedPolicy)
    assert aws_managed_policy.Arn == aws_managed_policy_arn


def test_aws_managed_policy_not_found():
    with pytest.raises(IAMManagedPolicyNotFoundException):
        IAMManagedPolicy.from_arn("not valid managed policy")
