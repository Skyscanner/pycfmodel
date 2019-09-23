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
from pycfmodel.model.resources.s3_bucket_policy import S3BucketPolicy

s3_bucket = {
    "S3BucketPolicy": {
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
}

s3_bucket_policy = S3BucketPolicy("S3BucketPolicy", s3_bucket["S3BucketPolicy"])


def test_generic_keys():
    assert s3_bucket_policy.bucket["Ref"] == "S3Bucket"


def test_policy_document():
    assert s3_bucket_policy.policy_document.statements is not None
