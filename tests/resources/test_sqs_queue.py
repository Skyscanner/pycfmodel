import pytest

from pycfmodel.model.resources.sqs_queue import SQSQueue


@pytest.fixture()
def valid_sqs_queue():
    return SQSQueue(
        **{
            "Type": "AWS::SQS::Queue",
            "Properties": {
                "QueueName": "my-queue",
                "VisibilityTimeout": 30,
                "MessageRetentionPeriod": 345600,
                "Tags": [{"Key": "Environment", "Value": "production"}],
            },
        }
    )


def test_valid_sqs_queue_resource(valid_sqs_queue):
    assert valid_sqs_queue.Properties.QueueName == "my-queue"
    assert valid_sqs_queue.Properties.VisibilityTimeout == 30
    assert valid_sqs_queue.Properties.MessageRetentionPeriod == 345600
    assert valid_sqs_queue.Properties.Tags[0].Key == "Environment"


def test_sqs_queue_with_fifo():
    queue = SQSQueue(
        **{
            "Type": "AWS::SQS::Queue",
            "Properties": {
                "QueueName": "my-queue.fifo",
                "FifoQueue": True,
                "ContentBasedDeduplication": True,
                "DeduplicationScope": "messageGroup",
                "FifoThroughputLimit": "perMessageGroupId",
            },
        }
    )
    assert queue.Properties.FifoQueue is True
    assert queue.Properties.ContentBasedDeduplication is True
    assert queue.Properties.DeduplicationScope == "messageGroup"


def test_sqs_queue_with_kms_encryption():
    queue = SQSQueue(
        **{
            "Type": "AWS::SQS::Queue",
            "Properties": {
                "QueueName": "my-encrypted-queue",
                "KmsMasterKeyId": "alias/aws/sqs",
                "KmsDataKeyReusePeriodSeconds": 300,
            },
        }
    )
    assert queue.Properties.KmsMasterKeyId == "alias/aws/sqs"
    assert queue.Properties.KmsDataKeyReusePeriodSeconds == 300


def test_sqs_queue_with_dead_letter_queue():
    queue = SQSQueue(
        **{
            "Type": "AWS::SQS::Queue",
            "Properties": {
                "QueueName": "my-queue",
                "RedrivePolicy": {
                    "deadLetterTargetArn": "arn:aws:sqs:us-east-1:123456789012:my-dlq",
                    "maxReceiveCount": 5,
                },
            },
        }
    )
    assert queue.Properties.RedrivePolicy["deadLetterTargetArn"] == "arn:aws:sqs:us-east-1:123456789012:my-dlq"


def test_sqs_queue_minimal():
    queue = SQSQueue(
        **{
            "Type": "AWS::SQS::Queue",
        }
    )
    assert queue.Type == "AWS::SQS::Queue"
    assert queue.Properties is not None
    assert queue.Properties.QueueName is None
