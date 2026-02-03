import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.elbv2_listener import ELBv2Listener


@pytest.fixture()
def valid_elbv2_listener():
    return ELBv2Listener(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::Listener",
            "Properties": {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234567890123456",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-tg/1234567890123456",
                    }
                ],
            },
        }
    )


def test_valid_elbv2_listener_resource(valid_elbv2_listener):
    assert valid_elbv2_listener.Properties.Port == 80
    assert valid_elbv2_listener.Properties.Protocol == "HTTP"
    assert len(valid_elbv2_listener.Properties.DefaultActions) == 1


def test_elbv2_listener_https():
    listener = ELBv2Listener(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::Listener",
            "Properties": {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234567890123456",
                "Port": 443,
                "Protocol": "HTTPS",
                "Certificates": [{"CertificateArn": "arn:aws:acm:us-east-1:123456789012:certificate/abc-123"}],
                "SslPolicy": "ELBSecurityPolicy-TLS-1-2-2017-01",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-tg/1234567890123456",
                    }
                ],
            },
        }
    )
    assert listener.Properties.Protocol == "HTTPS"
    assert listener.Properties.SslPolicy == "ELBSecurityPolicy-TLS-1-2-2017-01"
    assert len(listener.Properties.Certificates) == 1


def test_elbv2_listener_redirect_action():
    listener = ELBv2Listener(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::Listener",
            "Properties": {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234567890123456",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "redirect",
                        "RedirectConfig": {
                            "Protocol": "HTTPS",
                            "Port": "443",
                            "StatusCode": "HTTP_301",
                        },
                    }
                ],
            },
        }
    )
    assert listener.Properties.DefaultActions[0].Type == "redirect"
    assert listener.Properties.DefaultActions[0].RedirectConfig.StatusCode == "HTTP_301"


def test_elbv2_listener_fixed_response():
    listener = ELBv2Listener(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::Listener",
            "Properties": {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234567890123456",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "fixed-response",
                        "FixedResponseConfig": {
                            "StatusCode": "200",
                            "ContentType": "text/plain",
                            "MessageBody": "OK",
                        },
                    }
                ],
            },
        }
    )
    assert listener.Properties.DefaultActions[0].FixedResponseConfig.StatusCode == "200"


def test_elbv2_listener_forward_with_weights():
    listener = ELBv2Listener(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::Listener",
            "Properties": {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234567890123456",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "ForwardConfig": {
                            "TargetGroups": [
                                {
                                    "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/blue/1234567890123456",
                                    "Weight": 80,
                                },
                                {
                                    "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/green/1234567890123456",
                                    "Weight": 20,
                                },
                            ],
                            "TargetGroupStickinessConfig": {"Enabled": True, "DurationSeconds": 3600},
                        },
                    }
                ],
            },
        }
    )
    assert len(listener.Properties.DefaultActions[0].ForwardConfig.TargetGroups) == 2


def test_elbv2_listener_cognito_auth():
    listener = ELBv2Listener(
        **{
            "Type": "AWS::ElasticLoadBalancingV2::Listener",
            "Properties": {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234567890123456",
                "Port": 443,
                "Protocol": "HTTPS",
                "Certificates": [{"CertificateArn": "arn:aws:acm:us-east-1:123456789012:certificate/abc-123"}],
                "DefaultActions": [
                    {
                        "Type": "authenticate-cognito",
                        "Order": 1,
                        "AuthenticateCognitoConfig": {
                            "UserPoolArn": "arn:aws:cognito-idp:us-east-1:123456789012:userpool/us-east-1_abc123",
                            "UserPoolClientId": "client123",
                            "UserPoolDomain": "my-domain",
                        },
                    },
                    {
                        "Type": "forward",
                        "Order": 2,
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-tg/1234567890123456",
                    },
                ],
            },
        }
    )
    assert listener.Properties.DefaultActions[0].AuthenticateCognitoConfig.UserPoolDomain == "my-domain"


def test_elbv2_listener_requires_load_balancer_arn():
    with pytest.raises(ValidationError):
        ELBv2Listener(
            **{
                "Type": "AWS::ElasticLoadBalancingV2::Listener",
                "Properties": {
                    "Port": 80,
                    "Protocol": "HTTP",
                    "DefaultActions": [
                        {
                            "Type": "forward",
                            "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-tg/1234567890123456",
                        }
                    ],
                },
            }
        )


def test_elbv2_listener_requires_default_actions():
    with pytest.raises(ValidationError):
        ELBv2Listener(
            **{
                "Type": "AWS::ElasticLoadBalancingV2::Listener",
                "Properties": {
                    "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234567890123456",
                    "Port": 80,
                    "Protocol": "HTTP",
                },
            }
        )
