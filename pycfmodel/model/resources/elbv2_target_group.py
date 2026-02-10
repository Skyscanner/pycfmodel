"""
ELBv2TargetGroup resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::ElasticLoadBalancingV2::TargetGroup.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableModel, ResolvableStr


class Matcher(CustomModel):
    """
    Matcher configuration.
    """

    GrpcCode: Optional[ResolvableStr] = None
    HttpCode: Optional[ResolvableStr] = None


ResolvableMatcher = ResolvableModel(Matcher)


class TargetDescription(CustomModel):
    """
    TargetDescription configuration.
    """

    Id: ResolvableStr
    AvailabilityZone: Optional[ResolvableStr] = None
    Port: Optional[ResolvableInt] = None
    QuicServerId: Optional[ResolvableStr] = None


ResolvableTargetDescription = ResolvableModel(TargetDescription)


class TargetGroupAttribute(CustomModel):
    """
    TargetGroupAttribute configuration.
    """

    Key: Optional[ResolvableStr] = None
    Value: Optional[ResolvableStr] = None


ResolvableTargetGroupAttribute = ResolvableModel(TargetGroupAttribute)


class ELBv2TargetGroupProperties(CustomModel):
    """
    Properties for AWS::ElasticLoadBalancingV2::TargetGroup.

    Properties:

    - HealthCheckEnabled: Indicates whether health checks are enabled. If the target type is lambda, healt...
    - HealthCheckIntervalSeconds: The approximate amount of time, in seconds, between health checks of an individu...
    - HealthCheckPath: [HTTP/HTTPS health checks] The destination for health checks on the targets. [HT...
    - HealthCheckPort: The port the load balancer uses when performing health checks on targets.
    - HealthCheckProtocol: The protocol the load balancer uses when performing health checks on targets.
    - HealthCheckTimeoutSeconds: The amount of time, in seconds, during which no response from a target means a f...
    - HealthyThresholdCount: The number of consecutive health checks successes required before considering an...
    - IpAddressType: The type of IP address used for this target group. The possible values are ipv4 ...
    - Matcher: [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a suc...
    - Name: The name of the target group.
    - Port: The port on which the targets receive traffic. This port is used unless you spec...
    - Protocol: The protocol to use for routing traffic to the targets.
    - ProtocolVersion: [HTTP/HTTPS protocol] The protocol version. The possible values are GRPC, HTTP1,...
    - Tags: The tags.
    - TargetControlPort: The port that the target control agent uses to communicate the available capacit...
    - TargetGroupAttributes: The attributes.
    - TargetType: The type of target that you must specify when registering targets with this targ...
    - Targets: The targets.
    - UnhealthyThresholdCount: The number of consecutive health check failures required before considering a ta...
    - VpcId: The identifier of the virtual private cloud (VPC). If the target is a Lambda fun...

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html)
    """

    HealthCheckEnabled: Optional[ResolvableBool] = None
    HealthCheckIntervalSeconds: Optional[ResolvableInt] = None
    HealthCheckPath: Optional[ResolvableStr] = None
    HealthCheckPort: Optional[ResolvableStr] = None
    HealthCheckProtocol: Optional[ResolvableStr] = None
    HealthCheckTimeoutSeconds: Optional[ResolvableInt] = None
    HealthyThresholdCount: Optional[ResolvableInt] = None
    IpAddressType: Optional[ResolvableStr] = None
    Matcher: Optional[ResolvableMatcher] = None
    Name: Optional[ResolvableStr] = None
    Port: Optional[ResolvableInt] = None
    Protocol: Optional[ResolvableStr] = None
    ProtocolVersion: Optional[ResolvableStr] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    TargetControlPort: Optional[ResolvableInt] = None
    TargetGroupAttributes: Optional[Resolvable[List[TargetGroupAttribute]]] = None
    TargetType: Optional[ResolvableStr] = None
    Targets: Optional[Resolvable[List[TargetDescription]]] = None
    UnhealthyThresholdCount: Optional[ResolvableInt] = None
    VpcId: Optional[ResolvableStr] = None


class ELBv2TargetGroup(Resource):
    """
    Resource Type definition for AWS::ElasticLoadBalancingV2::TargetGroup

    Properties:

    - Properties: A [ELBv2TargetGroupProperties][pycfmodel.model.resources.elbv2_target_group.ELBv2TargetGroupProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html)
    """

    Type: Literal["AWS::ElasticLoadBalancingV2::TargetGroup"]
    Properties: Resolvable[ELBv2TargetGroupProperties] = ELBv2TargetGroupProperties()
