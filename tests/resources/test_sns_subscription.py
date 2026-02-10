import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.sns_subscription import SNSSubscription


@pytest.fixture()
def valid_sns_subscription():
    return SNSSubscription(
        **{
            "Type": "AWS::SNS::Subscription",
            "Properties": {
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
                "Protocol": "email",
                "Endpoint": "user@example.com",
            },
        }
    )


def test_valid_sns_subscription_resource(valid_sns_subscription):
    assert valid_sns_subscription.Properties.TopicArn == "arn:aws:sns:us-east-1:123456789012:my-topic"
    assert valid_sns_subscription.Properties.Protocol == "email"
    assert valid_sns_subscription.Properties.Endpoint == "user@example.com"


def test_sns_subscription_sqs_protocol():
    subscription = SNSSubscription(
        **{
            "Type": "AWS::SNS::Subscription",
            "Properties": {
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
                "Protocol": "sqs",
                "Endpoint": "arn:aws:sqs:us-east-1:123456789012:my-queue",
                "RawMessageDelivery": True,
            },
        }
    )
    assert subscription.Properties.Protocol == "sqs"
    assert subscription.Properties.RawMessageDelivery is True


def test_sns_subscription_lambda_protocol():
    subscription = SNSSubscription(
        **{
            "Type": "AWS::SNS::Subscription",
            "Properties": {
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
                "Protocol": "lambda",
                "Endpoint": "arn:aws:lambda:us-east-1:123456789012:function:my-function",
            },
        }
    )
    assert subscription.Properties.Protocol == "lambda"


def test_sns_subscription_with_filter_policy():
    subscription = SNSSubscription(
        **{
            "Type": "AWS::SNS::Subscription",
            "Properties": {
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
                "Protocol": "sqs",
                "Endpoint": "arn:aws:sqs:us-east-1:123456789012:my-queue",
                "FilterPolicy": {"event_type": ["order_placed", "order_cancelled"]},
                "FilterPolicyScope": "MessageBody",
            },
        }
    )
    assert subscription.Properties.FilterPolicy["event_type"] == ["order_placed", "order_cancelled"]
    assert subscription.Properties.FilterPolicyScope == "MessageBody"


def test_sns_subscription_with_redrive_policy():
    subscription = SNSSubscription(
        **{
            "Type": "AWS::SNS::Subscription",
            "Properties": {
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
                "Protocol": "sqs",
                "Endpoint": "arn:aws:sqs:us-east-1:123456789012:my-queue",
                "RedrivePolicy": {"deadLetterTargetArn": "arn:aws:sqs:us-east-1:123456789012:my-dlq"},
            },
        }
    )
    assert "deadLetterTargetArn" in subscription.Properties.RedrivePolicy


def test_sns_subscription_cross_region():
    subscription = SNSSubscription(
        **{
            "Type": "AWS::SNS::Subscription",
            "Properties": {
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
                "Protocol": "sqs",
                "Endpoint": "arn:aws:sqs:us-west-2:123456789012:my-queue",
                "Region": "us-east-1",
            },
        }
    )
    assert subscription.Properties.Region == "us-east-1"


def test_sns_subscription_requires_topic_arn():
    with pytest.raises(ValidationError):
        SNSSubscription(
            **{
                "Type": "AWS::SNS::Subscription",
                "Properties": {
                    "Protocol": "email",
                    "Endpoint": "user@example.com",
                },
            }
        )


def test_sns_subscription_requires_protocol():
    with pytest.raises(ValidationError):
        SNSSubscription(
            **{
                "Type": "AWS::SNS::Subscription",
                "Properties": {
                    "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
                    "Endpoint": "user@example.com",
                },
            }
        )
