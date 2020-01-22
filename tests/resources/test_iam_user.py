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

from pycfmodel.model.resources.iam_user import IAMUser


@pytest.fixture()
def iam_user():
    return IAMUser(
        **{
            "Type": "AWS::IAM::User",
            "Properties": {
                "Path": "/",
                "UserName": "TestUser",
                "LoginProfile": {"Password": "ThisMyBestP@ssword", "PasswordResetRequired": False},
                "Policies": [
                    {
                        "PolicyName": "BadPolicy",
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Action": ["lambda:AddPermission", "ssm:SendCommand", "kms:Decrypt"],
                                    "Resource": "*",
                                }
                            ],
                        },
                    }
                ],
            },
        }
    )


def test_policies(iam_user):
    assert len(iam_user.Properties.Policies) == 1
    assert iam_user.Properties.Policies[0].PolicyName == "BadPolicy"


def test_credential_check(iam_user):
    assert iam_user.has_hardcoded_credentials()
