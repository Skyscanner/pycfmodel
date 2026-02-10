import json

import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.s3_bucket import S3Bucket


@pytest.fixture()
def valid_s3_bucket():
    return S3Bucket(
        **{
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "AccessControl": "Private",
                "VersioningConfiguration": {"Status": "Enabled"},
                "Tags": [{"Key": "Project", "Value": "test"}],
                "ReplicationConfiguration": {
                    "Role": "arn:aws:iam::123456789012:role/replication_role",
                    "Rules": [
                        {
                            "Id": "MyRule1",
                            "Status": "Enabled",
                            "Prefix": "MyPrefix",
                            "Destination": {"Bucket": "arn:aws:s3:::my-replication-bucket", "StorageClass": "STANDARD"},
                        },
                        {
                            "Status": "Enabled",
                            "Prefix": "MyOtherPrefix",
                            "Destination": {"Bucket": "arn:aws:s3:::my-replication-bucket"},
                        },
                    ],
                },
            },
        }
    )


def test_valid_s3_bucket_resource(valid_s3_bucket):
    assert valid_s3_bucket.Properties.ReplicationConfiguration.Role == "arn:aws:iam::123456789012:role/replication_role"
    assert valid_s3_bucket.Properties.ReplicationConfiguration.Rules[1].Status == "Enabled"
    assert valid_s3_bucket.Properties.VersioningConfiguration.Status == "Enabled"
    assert valid_s3_bucket.Properties.Tags[0].Value == "test"


def test_s3_bucket_lifecycle_with_transitions():
    """
    Regression test: Transitions and NoncurrentVersionTransitions in lifecycle rules
    must be parsed correctly as List[Transition] and List[NoncurrentVersionTransition],
    not as List[NoneType] due to field name shadowing in the Rule class body.
    """
    bucket = S3Bucket(
        **{
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "LifecycleConfiguration": {
                    "Rules": [
                        {
                            "Id": "expire-rule",
                            "Status": "Enabled",
                            "ExpirationInDays": 90,
                        },
                        {
                            "Id": "transition-rule",
                            "Status": "Enabled",
                            "Transitions": [
                                {"StorageClass": "STANDARD_IA", "TransitionInDays": 30},
                                {"StorageClass": "GLACIER", "TransitionInDays": 90},
                            ],
                            "NoncurrentVersionTransitions": [
                                {"StorageClass": "GLACIER", "TransitionInDays": 60},
                            ],
                        },
                    ]
                }
            },
        }
    )

    rules = bucket.Properties.LifecycleConfiguration.Rules
    assert len(rules) == 2

    assert rules[0].Transitions is None
    assert rules[0].ExpirationInDays == 90

    assert len(rules[1].Transitions) == 2
    assert rules[1].Transitions[0].StorageClass == "STANDARD_IA"
    assert rules[1].Transitions[0].TransitionInDays == 30
    assert rules[1].Transitions[1].StorageClass == "GLACIER"
    assert rules[1].Transitions[1].TransitionInDays == 90

    assert len(rules[1].NoncurrentVersionTransitions) == 1
    assert rules[1].NoncurrentVersionTransitions[0].StorageClass == "GLACIER"
    assert rules[1].NoncurrentVersionTransitions[0].TransitionInDays == 60


def test_extra_fields_not_allowed_s3_bucket():
    with pytest.raises(ValidationError) as exc_info:
        S3Bucket(
            **{
                "Type": "AWS::S3::Bucket",
                "Properties": {"AccelerateConfiguration": "None", "AnalyticsConfigurations": {"a": "b"}, "foo": "bar"},
            }
        )

    errors = json.loads(exc_info.value.json())
    error_locs = [tuple(e["loc"]) for e in errors]

    # Check that extra field 'foo' is rejected
    assert any("foo" in loc for loc in error_locs)

    # Check that invalid AccelerateConfiguration is rejected
    assert any("AccelerateConfiguration" in loc for loc in error_locs)

    # Check that invalid AnalyticsConfigurations is rejected
    assert any("AnalyticsConfigurations" in loc for loc in error_locs)
