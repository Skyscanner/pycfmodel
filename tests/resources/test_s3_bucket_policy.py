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

from pycfmodel.model.resources.s3_bucket_policy import S3BucketPolicy


@pytest.fixture()
def s3_bucket_policy():
    return S3BucketPolicy(
        **{
            "Type": "AWS::S3::BucketPolicy",
            "Properties": {
                "Bucket": {"Ref": "S3Bucket"},
                "PolicyDocument": {
                    "Statement": [
                        {
                            "Action": ["*"],
                            "Effect": "Allow",
                            "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                            "Principal": {"AWS": ["156460612806"]},
                        }
                    ]
                },
            },
        }
    )


def test_policy_document(s3_bucket_policy):
    assert s3_bucket_policy.Properties.PolicyDocument.Statement[0].Action[0] == "*"
