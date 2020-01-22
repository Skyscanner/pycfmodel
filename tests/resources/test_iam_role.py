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

from pycfmodel.model.resources.iam_role import IAMRole


@pytest.fixture()
def iam_role():
    return IAMRole(
        **{
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": {
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"], "AWS": "arn:aws:iam::111111111111:root"},
                        "Action": ["sts:AssumeRole"],
                    },
                },
                "Path": "/",
                "Policies": [
                    {
                        "PolicyName": "root",
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": {"Effect": "Allow", "Action": "*", "Resource": "*"},
                        },
                    }
                ],
            },
        }
    )


def test_policies(iam_role):
    policies = iam_role.Properties.Policies
    assert len(policies) == 1
    assert policies[0].PolicyName == "root"
