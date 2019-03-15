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


from pycfmodel.model.resources.iam_user import IAMUser

cf_script = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "myuser": {
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
                                        "Action": [
                                            "lambda:AddPermission",
                                            "ssm:SendCommand",
                                            "kms:Decrypt"
                                        ],
                                        "Resource": "*"
                                    }
                                ]
                            }
                        }
                ]
            }
        }
    }
}


iam_user = IAMUser("myuser", cf_script["Resources"]["myuser"])


def test_policies():
    assert len(iam_user.policies) == 1
    policy = iam_user.policies[0]
    assert policy.policy_name == "BadPolicy"


def test_credential_check():
    assert iam_user.has_hardcoded_credentials()
