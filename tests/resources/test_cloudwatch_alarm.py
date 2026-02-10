import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.cloudwatch_alarm import CloudWatchAlarm


@pytest.fixture()
def valid_cloudwatch_alarm():
    return CloudWatchAlarm(
        **{
            "Type": "AWS::CloudWatch::Alarm",
            "Properties": {
                "AlarmName": "high-cpu-alarm",
                "AlarmDescription": "Alarm when CPU exceeds 80%",
                "MetricName": "CPUUtilization",
                "Namespace": "AWS/EC2",
                "Statistic": "Average",
                "Period": 300,
                "EvaluationPeriods": 2,
                "Threshold": 80,
                "ComparisonOperator": "GreaterThanThreshold",
            },
        }
    )


def test_valid_cloudwatch_alarm_resource(valid_cloudwatch_alarm):
    assert valid_cloudwatch_alarm.Properties.AlarmName == "high-cpu-alarm"
    assert valid_cloudwatch_alarm.Properties.MetricName == "CPUUtilization"
    assert valid_cloudwatch_alarm.Properties.Namespace == "AWS/EC2"
    assert valid_cloudwatch_alarm.Properties.Threshold == 80
    assert valid_cloudwatch_alarm.Properties.ComparisonOperator == "GreaterThanThreshold"


def test_cloudwatch_alarm_with_dimensions():
    alarm = CloudWatchAlarm(
        **{
            "Type": "AWS::CloudWatch::Alarm",
            "Properties": {
                "AlarmName": "instance-cpu-alarm",
                "MetricName": "CPUUtilization",
                "Namespace": "AWS/EC2",
                "EvaluationPeriods": 1,
                "ComparisonOperator": "GreaterThanThreshold",
                "Dimensions": [{"Name": "InstanceId", "Value": "i-1234567890abcdef0"}],
                "Period": 60,
                "Statistic": "Average",
                "Threshold": 90,
            },
        }
    )
    assert len(alarm.Properties.Dimensions) == 1
    assert alarm.Properties.Dimensions[0].Name == "InstanceId"


def test_cloudwatch_alarm_with_actions():
    alarm = CloudWatchAlarm(
        **{
            "Type": "AWS::CloudWatch::Alarm",
            "Properties": {
                "AlarmName": "cpu-alarm",
                "MetricName": "CPUUtilization",
                "Namespace": "AWS/EC2",
                "EvaluationPeriods": 1,
                "ComparisonOperator": "GreaterThanThreshold",
                "AlarmActions": ["arn:aws:sns:us-east-1:123456789012:my-topic"],
                "OKActions": ["arn:aws:sns:us-east-1:123456789012:my-topic"],
                "InsufficientDataActions": ["arn:aws:sns:us-east-1:123456789012:my-topic"],
            },
        }
    )
    assert len(alarm.Properties.AlarmActions) == 1
    assert len(alarm.Properties.OKActions) == 1


def test_cloudwatch_alarm_with_metric_math():
    alarm = CloudWatchAlarm(
        **{
            "Type": "AWS::CloudWatch::Alarm",
            "Properties": {
                "AlarmName": "metric-math-alarm",
                "EvaluationPeriods": 1,
                "ComparisonOperator": "GreaterThanThreshold",
                "Threshold": 100,
                "Metrics": [
                    {
                        "Id": "e1",
                        "Expression": "m1 + m2",
                        "Label": "Sum of metrics",
                        "ReturnData": True,
                    },
                    {
                        "Id": "m1",
                        "MetricStat": {
                            "Metric": {"MetricName": "Metric1", "Namespace": "Custom"},
                            "Period": 60,
                            "Stat": "Sum",
                        },
                        "ReturnData": False,
                    },
                ],
            },
        }
    )
    assert len(alarm.Properties.Metrics) == 2
    assert alarm.Properties.Metrics[0].Expression == "m1 + m2"


def test_cloudwatch_alarm_requires_comparison_operator():
    with pytest.raises(ValidationError):
        CloudWatchAlarm(
            **{
                "Type": "AWS::CloudWatch::Alarm",
                "Properties": {
                    "AlarmName": "my-alarm",
                    "EvaluationPeriods": 1,
                },
            }
        )


def test_cloudwatch_alarm_requires_evaluation_periods():
    with pytest.raises(ValidationError):
        CloudWatchAlarm(
            **{
                "Type": "AWS::CloudWatch::Alarm",
                "Properties": {
                    "AlarmName": "my-alarm",
                    "ComparisonOperator": "GreaterThanThreshold",
                },
            }
        )
