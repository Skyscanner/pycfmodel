import pytest

from pycfmodel.model.resources.sns_topic import SNSTopic


@pytest.fixture()
def valid_sns_topic():
    return SNSTopic(
        **{
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": "my-topic",
                "DisplayName": "My Topic",
                "FifoTopic": False,
                "Tags": [{"Key": "Environment", "Value": "production"}],
            },
        }
    )


def test_valid_sns_topic_resource(valid_sns_topic):
    assert valid_sns_topic.Properties.TopicName == "my-topic"
    assert valid_sns_topic.Properties.DisplayName == "My Topic"
    assert valid_sns_topic.Properties.FifoTopic is False
    assert valid_sns_topic.Properties.Tags[0].Key == "Environment"


def test_sns_topic_with_fifo():
    topic = SNSTopic(
        **{
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": "my-topic.fifo",
                "FifoTopic": True,
                "ContentBasedDeduplication": True,
            },
        }
    )
    assert topic.Properties.FifoTopic is True
    assert topic.Properties.ContentBasedDeduplication is True


def test_sns_topic_with_delivery_status_logging():
    topic = SNSTopic(
        **{
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": "my-topic",
                "DeliveryStatusLogging": [
                    {
                        "Protocol": "sqs",
                        "SuccessFeedbackRoleArn": "arn:aws:iam::123456789012:role/SNSSuccessFeedback",
                        "FailureFeedbackRoleArn": "arn:aws:iam::123456789012:role/SNSFailureFeedback",
                    },
                ],
            },
        }
    )
    assert len(topic.Properties.DeliveryStatusLogging) == 1
    assert topic.Properties.DeliveryStatusLogging[0].Protocol == "sqs"


def test_sns_topic_with_kms_encryption():
    topic = SNSTopic(
        **{
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": "my-encrypted-topic",
                "KmsMasterKeyId": "alias/aws/sns",
            },
        }
    )
    assert topic.Properties.KmsMasterKeyId == "alias/aws/sns"


def test_sns_topic_minimal():
    topic = SNSTopic(
        **{
            "Type": "AWS::SNS::Topic",
        }
    )
    assert topic.Type == "AWS::SNS::Topic"
    assert topic.Properties is None
