import pytest

from pycfmodel.model.resources.properties.statement_condition import StatementCondition
from pycfmodel.model.resources.s3_bucket_policy import S3BucketPolicy
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


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
                            "Condition": {"StringNotEquals": {"s3:VersionId": "AaaHbAQitwiL_h47_44lRO2DDfLlBO5e"}},
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


def test_s3_bucketpolicy_policy_document_property(s3_bucket_policy):
    assert s3_bucket_policy.policy_documents == [
        OptionallyNamedPolicyDocument(name=None, policy_document=s3_bucket_policy.Properties.PolicyDocument)
    ]


def test_s3_bucketpolicy_all_statement_conditions(s3_bucket_policy):
    assert s3_bucket_policy.all_statement_conditions == [
        StatementCondition(StringNotEquals={"s3:VersionId": "AaaHbAQitwiL_h47_44lRO2DDfLlBO5e"})
    ]
