import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.dynamodb_table import DynamoDBTable


@pytest.fixture()
def valid_dynamodb_table():
    return DynamoDBTable(
        **{
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "TableName": "my-table",
                "KeySchema": [
                    {"AttributeName": "pk", "KeyType": "HASH"},
                    {"AttributeName": "sk", "KeyType": "RANGE"},
                ],
                "AttributeDefinitions": [
                    {"AttributeName": "pk", "AttributeType": "S"},
                    {"AttributeName": "sk", "AttributeType": "S"},
                ],
                "BillingMode": "PAY_PER_REQUEST",
            },
        }
    )


def test_valid_dynamodb_table_resource(valid_dynamodb_table):
    assert valid_dynamodb_table.Properties.TableName == "my-table"
    assert len(valid_dynamodb_table.Properties.KeySchema) == 2
    assert valid_dynamodb_table.Properties.KeySchema[0].AttributeName == "pk"
    assert valid_dynamodb_table.Properties.BillingMode == "PAY_PER_REQUEST"


def test_dynamodb_table_with_provisioned_throughput():
    table = DynamoDBTable(
        **{
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "TableName": "my-table",
                "KeySchema": [{"AttributeName": "pk", "KeyType": "HASH"}],
                "AttributeDefinitions": [{"AttributeName": "pk", "AttributeType": "S"}],
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            },
        }
    )
    assert table.Properties.ProvisionedThroughput.ReadCapacityUnits == 5
    assert table.Properties.ProvisionedThroughput.WriteCapacityUnits == 5


def test_dynamodb_table_with_gsi():
    table = DynamoDBTable(
        **{
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "TableName": "my-table",
                "KeySchema": [{"AttributeName": "pk", "KeyType": "HASH"}],
                "AttributeDefinitions": [
                    {"AttributeName": "pk", "AttributeType": "S"},
                    {"AttributeName": "gsi_pk", "AttributeType": "S"},
                ],
                "BillingMode": "PAY_PER_REQUEST",
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": "gsi-index",
                        "KeySchema": [{"AttributeName": "gsi_pk", "KeyType": "HASH"}],
                        "Projection": {"ProjectionType": "ALL"},
                    }
                ],
            },
        }
    )
    assert len(table.Properties.GlobalSecondaryIndexes) == 1
    assert table.Properties.GlobalSecondaryIndexes[0].IndexName == "gsi-index"


def test_dynamodb_table_with_stream():
    table = DynamoDBTable(
        **{
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "TableName": "my-table",
                "KeySchema": [{"AttributeName": "pk", "KeyType": "HASH"}],
                "AttributeDefinitions": [{"AttributeName": "pk", "AttributeType": "S"}],
                "BillingMode": "PAY_PER_REQUEST",
                "StreamSpecification": {"StreamViewType": "NEW_AND_OLD_IMAGES"},
            },
        }
    )
    assert table.Properties.StreamSpecification.StreamViewType == "NEW_AND_OLD_IMAGES"


def test_dynamodb_table_with_ttl():
    table = DynamoDBTable(
        **{
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "TableName": "my-table",
                "KeySchema": [{"AttributeName": "pk", "KeyType": "HASH"}],
                "AttributeDefinitions": [{"AttributeName": "pk", "AttributeType": "S"}],
                "BillingMode": "PAY_PER_REQUEST",
                "TimeToLiveSpecification": {"AttributeName": "ttl", "Enabled": True},
            },
        }
    )
    assert table.Properties.TimeToLiveSpecification.Enabled is True
    assert table.Properties.TimeToLiveSpecification.AttributeName == "ttl"


def test_dynamodb_table_with_sse():
    table = DynamoDBTable(
        **{
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "TableName": "my-table",
                "KeySchema": [{"AttributeName": "pk", "KeyType": "HASH"}],
                "AttributeDefinitions": [{"AttributeName": "pk", "AttributeType": "S"}],
                "BillingMode": "PAY_PER_REQUEST",
                "SSESpecification": {"SSEEnabled": True, "SSEType": "KMS"},
            },
        }
    )
    assert table.Properties.SSESpecification.SSEEnabled is True


def test_dynamodb_table_requires_key_schema():
    with pytest.raises(ValidationError):
        DynamoDBTable(
            **{
                "Type": "AWS::DynamoDB::Table",
                "Properties": {
                    "TableName": "my-table",
                    "BillingMode": "PAY_PER_REQUEST",
                },
            }
        )
