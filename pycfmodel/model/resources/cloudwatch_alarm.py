"""
CloudWatchAlarm resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::CloudWatch::Alarm.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable
from pycfmodel.model.types import ResolvableBool
from pycfmodel.model.types import ResolvableInt
from pycfmodel.model.types import ResolvableModel
from pycfmodel.model.types import ResolvableStr


class Dimension(CustomModel):
    """
    Dimension is an embedded property of the ``AWS::CloudWatch::Alarm`` type.
    """

    Name: ResolvableStr
    Value: ResolvableStr


ResolvableDimension = ResolvableModel(Dimension)


class Metric(CustomModel):
    """
    The ``Metric`` property type represents a specific metric.
    """

    Dimensions: Optional[Resolvable[List[Dimension]]] = None
    MetricName: Optional[ResolvableStr] = None
    Namespace: Optional[ResolvableStr] = None


ResolvableMetric = ResolvableModel(Metric)


class MetricStat(CustomModel):
    """
    This structure defines the metric to be returned, along with the statistics, period, and units.
    """

    Metric: ResolvableMetric
    Period: ResolvableInt
    Stat: ResolvableStr
    Unit: Optional[ResolvableStr] = None


ResolvableMetricStat = ResolvableModel(MetricStat)


class MetricDataQuery(CustomModel):
    """
    The ``MetricDataQuery`` property type specifies the metric data to return, and whether this call is just retrieving a batch set of data for one metric, or is performing a math expression on metric data.
    """

    Id: ResolvableStr
    AccountId: Optional[ResolvableStr] = None
    Expression: Optional[ResolvableStr] = None
    Label: Optional[ResolvableStr] = None
    MetricStat: Optional[ResolvableMetricStat] = None
    Period: Optional[ResolvableInt] = None
    ReturnData: Optional[ResolvableBool] = None


ResolvableMetricDataQuery = ResolvableModel(MetricDataQuery)


class Tag(CustomModel):
    """
    One of the key-value pairs associated with the alarm.
    """

    Key: ResolvableStr
    Value: ResolvableStr


ResolvableTag = ResolvableModel(Tag)


class CloudWatchAlarmProperties(CustomModel):
    """
    Properties for AWS::CloudWatch::Alarm.

    Properties:

    - ActionsEnabled: Indicates whether actions should be executed during any changes to the alarm sta...
    - AlarmActions: The list of actions to execute when this alarm transitions into an ALARM state f...
    - AlarmDescription: The description of the alarm.
    - AlarmName: The name of the alarm. If you don't specify a name, CFN generates a unique physi...
    - ComparisonOperator: The arithmetic operation to use when comparing the specified statistic and thres...
    - DatapointsToAlarm: The number of datapoints that must be breaching to trigger the alarm. This is us...
    - Dimensions: The dimensions for the metric associated with the alarm. For an alarm based on a...
    - EvaluateLowSampleCountPercentile: Used only for alarms based on percentiles. If ``ignore``, the alarm state does n...
    - EvaluationPeriods: The number of periods over which data is compared to the specified threshold. If...
    - ExtendedStatistic: The percentile statistic for the metric associated with the alarm. Specify a val...
    - InsufficientDataActions: The actions to execute when this alarm transitions to the ``INSUFFICIENT_DATA`` ...
    - MetricName: The name of the metric associated with the alarm. This is required for an alarm ...
    - Metrics: An array that enables you to create an alarm based on the result of a metric mat...
    - Namespace: The namespace of the metric associated with the alarm. This is required for an a...
    - OKActions: The actions to execute when this alarm transitions to the ``OK`` state from any ...
    - Period: The period, in seconds, over which the statistic is applied. This is required fo...
    - Statistic: The statistic for the metric associated with the alarm, other than percentile. F...
    - Tags: A list of key-value pairs to associate with the alarm. You can associate as many...
    - Threshold: The value to compare with the specified statistic.
    - ThresholdMetricId: In an alarm based on an anomaly detection model, this is the ID of the ``ANOMALY...
    - TreatMissingData: Sets how this alarm is to handle missing data points. Valid values are ``breachi...
    - Unit: The unit of the metric associated with the alarm. Specify this only if you are c...

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html)
    """

    ComparisonOperator: ResolvableStr
    EvaluationPeriods: ResolvableInt
    ActionsEnabled: Optional[ResolvableBool] = None
    AlarmActions: Optional[Resolvable[List[ResolvableStr]]] = None
    AlarmDescription: Optional[ResolvableStr] = None
    AlarmName: Optional[ResolvableStr] = None
    DatapointsToAlarm: Optional[ResolvableInt] = None
    Dimensions: Optional[Resolvable[List[Dimension]]] = None
    EvaluateLowSampleCountPercentile: Optional[ResolvableStr] = None
    ExtendedStatistic: Optional[ResolvableStr] = None
    InsufficientDataActions: Optional[Resolvable[List[ResolvableStr]]] = None
    MetricName: Optional[ResolvableStr] = None
    Metrics: Optional[Resolvable[List[MetricDataQuery]]] = None
    Namespace: Optional[ResolvableStr] = None
    OKActions: Optional[Resolvable[List[ResolvableStr]]] = None
    Period: Optional[ResolvableInt] = None
    Statistic: Optional[ResolvableStr] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    Threshold: Optional[ResolvableInt] = None
    ThresholdMetricId: Optional[ResolvableStr] = None
    TreatMissingData: Optional[ResolvableStr] = None
    Unit: Optional[ResolvableStr] = None


class CloudWatchAlarm(Resource):
    """
    The ``AWS::CloudWatch::Alarm`` type specifies an alarm and associates it with the specified metric or metric math expression.

    Properties:

    - Properties: A [CloudWatchAlarmProperties][pycfmodel.model.resources.cloudwatch_alarm.CloudWatchAlarmProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html)
    """

    Type: Literal["AWS::CloudWatch::Alarm"]
    Properties: Resolvable[CloudWatchAlarmProperties]
