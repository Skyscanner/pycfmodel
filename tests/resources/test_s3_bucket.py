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

    assert json.loads(exc_info.value.json()) == [
        {
            "ctx": {"error": "Not supported type: <class 'str'>"},
            "input": "None",
            "loc": ["Properties", "S3BucketProperties", "AccelerateConfiguration", "Generic"],
            "msg": "Value error, Not supported type: <class 'str'>",
            "type": "value_error",
            "url": "https://errors.pydantic.dev/2.7/v/value_error",
        },
        {
            "ctx": {"error": "FunctionDict should only have 1 key and be a function"},
            "input": "None",
            "loc": ["Properties", "S3BucketProperties", "AccelerateConfiguration", "FunctionDict"],
            "msg": "Value error, FunctionDict should only have 1 key and be a function",
            "type": "value_error",
            "url": "https://errors.pydantic.dev/2.7/v/value_error",
        },
        {
            "input": {"a": "b"},
            "loc": ["Properties", "S3BucketProperties", "AnalyticsConfigurations", "list[union[Generic,FunctionDict]]"],
            "msg": "Input should be a valid list",
            "type": "list_type",
            "url": "https://errors.pydantic.dev/2.7/v/list_type",
        },
        {
            "ctx": {"error": "FunctionDict should only have 1 key and be a function"},
            "input": {"a": "b"},
            "loc": ["Properties", "S3BucketProperties", "AnalyticsConfigurations", "FunctionDict"],
            "msg": "Value error, FunctionDict should only have 1 key and be a function",
            "type": "value_error",
            "url": "https://errors.pydantic.dev/2.7/v/value_error",
        },
        {
            "input": "bar",
            "loc": ["Properties", "S3BucketProperties", "foo"],
            "msg": "Extra inputs are not permitted",
            "type": "extra_forbidden",
            "url": "https://errors.pydantic.dev/2.7/v/extra_forbidden",
        },
        {
            "ctx": {"error": "FunctionDict should only have 1 key and be a function"},
            "input": {"AccelerateConfiguration": "None", "AnalyticsConfigurations": {"a": "b"}, "foo": "bar"},
            "loc": ["Properties", "FunctionDict"],
            "msg": "Value error, FunctionDict should only have 1 key and be a function",
            "type": "value_error",
            "url": "https://errors.pydantic.dev/2.7/v/value_error",
        },
    ]
