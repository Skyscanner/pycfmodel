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
