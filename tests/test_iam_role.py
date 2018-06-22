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


from pycfmodel.model.resources.iam_role import IAMRole

cf_script = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "RootRole": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": ["ec2.amazonaws.com"],
                            "AWS": "arn:aws:iam::111111111111:root"
                        },
                        "Action": ["sts:AssumeRole"]
                    }
                },
                "Path": "/",
                "Policies": [
                    {
                        "PolicyName": "root",
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": "*",
                                "Resource": "*"
                            }
                        }
                    }
                ]
            }
        }
    }
}


iam_role = IAMRole("RootRole", cf_script["Resources"]["RootRole"])


def test_policies():
    assert len(iam_role.policies) == 1
    policy = iam_role.policies[0]

    assert policy.policy_name == "root"
