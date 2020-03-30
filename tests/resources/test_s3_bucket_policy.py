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
