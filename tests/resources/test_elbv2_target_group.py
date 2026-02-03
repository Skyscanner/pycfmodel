import pytest

from pycfmodel.model.resources.elbv2_target_group import ELBv2TargetGroup


@pytest.fixture()
def valid_elbv2_target_group():
    return ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "my-target-group",
                "Port": 80,
                "Protocol": "HTTP",
                "VpcId": "vpc-1234567890abcdef0",
                "TargetType": "instance",
            },
        }
    )


def test_valid_elbv2_target_group_resource(valid_elbv2_target_group):
    assert valid_elbv2_target_group.Properties.Name == "my-target-group"
    assert valid_elbv2_target_group.Properties.Port == 80
    assert valid_elbv2_target_group.Properties.Protocol == "HTTP"
    assert valid_elbv2_target_group.Properties.TargetType == "instance"


def test_elbv2_target_group_ip_target():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "ip-target-group",
                "Port": 80,
                "Protocol": "HTTP",
                "VpcId": "vpc-1234567890abcdef0",
                "TargetType": "ip",
                "IpAddressType": "ipv4",
            },
        }
    )
    assert target_group.Properties.TargetType == "ip"
    assert target_group.Properties.IpAddressType == "ipv4"


def test_elbv2_target_group_lambda_target():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "lambda-target-group",
                "TargetType": "lambda",
                "Targets": [{"Id": "arn:aws:lambda:us-east-1:123456789012:function:my-function"}],
            },
        }
    )
    assert target_group.Properties.TargetType == "lambda"
    assert len(target_group.Properties.Targets) == 1


def test_elbv2_target_group_health_check():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "my-target-group",
                "Port": 80,
                "Protocol": "HTTP",
                "VpcId": "vpc-1234567890abcdef0",
                "HealthCheckEnabled": True,
                "HealthCheckPath": "/health",
                "HealthCheckPort": "traffic-port",
                "HealthCheckProtocol": "HTTP",
                "HealthCheckIntervalSeconds": 30,
                "HealthCheckTimeoutSeconds": 5,
                "HealthyThresholdCount": 3,
                "UnhealthyThresholdCount": 2,
            },
        }
    )
    assert target_group.Properties.HealthCheckEnabled is True
    assert target_group.Properties.HealthCheckPath == "/health"
    assert target_group.Properties.HealthCheckIntervalSeconds == 30


def test_elbv2_target_group_with_matcher():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "my-target-group",
                "Port": 80,
                "Protocol": "HTTP",
                "VpcId": "vpc-1234567890abcdef0",
                "Matcher": {"HttpCode": "200-299"},
            },
        }
    )
    assert target_group.Properties.Matcher.HttpCode == "200-299"


def test_elbv2_target_group_grpc():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "grpc-target-group",
                "Port": 50051,
                "Protocol": "HTTP",
                "ProtocolVersion": "GRPC",
                "VpcId": "vpc-1234567890abcdef0",
                "Matcher": {"GrpcCode": "0-99"},
            },
        }
    )
    assert target_group.Properties.ProtocolVersion == "GRPC"
    assert target_group.Properties.Matcher.GrpcCode == "0-99"


def test_elbv2_target_group_with_attributes():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "my-target-group",
                "Port": 80,
                "Protocol": "HTTP",
                "VpcId": "vpc-1234567890abcdef0",
                "TargetGroupAttributes": [
                    {"Key": "deregistration_delay.timeout_seconds", "Value": "300"},
                    {"Key": "stickiness.enabled", "Value": "true"},
                ],
            },
        }
    )
    assert len(target_group.Properties.TargetGroupAttributes) == 2


def test_elbv2_target_group_with_tags():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
            "Properties": {
                "Name": "my-target-group",
                "Port": 80,
                "Protocol": "HTTP",
                "VpcId": "vpc-1234567890abcdef0",
                "Tags": [{"Key": "Environment", "Value": "production"}],
            },
        }
    )
    assert target_group.Properties.Tags[0].Key == "Environment"


def test_elbv2_target_group_minimal():
    target_group = ELBv2TargetGroup(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
        }
    )
    assert target_group.Type == "AWS::ElasticLoadBalancingV2::TargetGroup"
    assert target_group.Properties is None
