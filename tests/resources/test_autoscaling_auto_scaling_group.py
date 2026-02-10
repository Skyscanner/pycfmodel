import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.autoscaling_auto_scaling_group import AutoScalingAutoScalingGroup


@pytest.fixture()
def valid_autoscaling_group():
    return AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "AutoScalingGroupName": "my-asg",
                "MinSize": "1",
                "MaxSize": "10",
                "DesiredCapacity": "2",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-1234567890abcdef0",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-1234567890abcdef0", "subnet-0987654321fedcba0"],
            },
        }
    )


def test_valid_autoscaling_group_resource(valid_autoscaling_group):
    assert valid_autoscaling_group.Properties.AutoScalingGroupName == "my-asg"
    assert valid_autoscaling_group.Properties.MinSize == "1"
    assert valid_autoscaling_group.Properties.MaxSize == "10"
    assert valid_autoscaling_group.Properties.DesiredCapacity == "2"


def test_autoscaling_group_with_launch_configuration():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchConfigurationName": "my-launch-config",
                "AvailabilityZones": ["us-east-1a", "us-east-1b"],
            },
        }
    )
    assert asg.Properties.LaunchConfigurationName == "my-launch-config"
    assert len(asg.Properties.AvailabilityZones) == 2


def test_autoscaling_group_with_mixed_instances_policy():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "10",
                "VPCZoneIdentifier": ["subnet-123"],
                "MixedInstancesPolicy": {
                    "LaunchTemplate": {
                        "LaunchTemplateSpecification": {
                            "LaunchTemplateId": "lt-123",
                            "Version": "$Latest",
                        },
                        "Overrides": [
                            {"InstanceType": "t3.micro"},
                            {"InstanceType": "t3.small"},
                            {"InstanceType": "t3.medium"},
                        ],
                    },
                    "InstancesDistribution": {
                        "OnDemandBaseCapacity": 1,
                        "OnDemandPercentageAboveBaseCapacity": 25,
                        "SpotAllocationStrategy": "capacity-optimized",
                    },
                },
            },
        }
    )
    assert len(asg.Properties.MixedInstancesPolicy.LaunchTemplate.Overrides) == 3
    assert asg.Properties.MixedInstancesPolicy.InstancesDistribution.OnDemandBaseCapacity == 1


def test_autoscaling_group_with_target_groups():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-123",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-123"],
                "TargetGroupARNs": [
                    "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-tg/1234567890123456"
                ],
            },
        }
    )
    assert len(asg.Properties.TargetGroupARNs) == 1


def test_autoscaling_group_with_health_check():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-123",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-123"],
                "HealthCheckType": "ELB",
                "HealthCheckGracePeriod": 300,
            },
        }
    )
    assert asg.Properties.HealthCheckType == "ELB"
    assert asg.Properties.HealthCheckGracePeriod == 300


def test_autoscaling_group_with_lifecycle_hooks():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-123",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-123"],
                "LifecycleHookSpecificationList": [
                    {
                        "LifecycleHookName": "launch-hook",
                        "LifecycleTransition": "autoscaling:EC2_INSTANCE_LAUNCHING",
                        "DefaultResult": "CONTINUE",
                        "HeartbeatTimeout": 300,
                    }
                ],
            },
        }
    )
    assert len(asg.Properties.LifecycleHookSpecificationList) == 1
    assert asg.Properties.LifecycleHookSpecificationList[0].LifecycleHookName == "launch-hook"


def test_autoscaling_group_with_notification():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-123",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-123"],
                "NotificationConfiguration": {
                    "TopicARN": "arn:aws:sns:us-east-1:123456789012:my-topic",
                    "NotificationTypes": [
                        "autoscaling:EC2_INSTANCE_LAUNCH",
                        "autoscaling:EC2_INSTANCE_TERMINATE",
                    ],
                },
            },
        }
    )
    assert asg.Properties.NotificationConfiguration.TopicARN == "arn:aws:sns:us-east-1:123456789012:my-topic"


def test_autoscaling_group_with_notification_configurations():
    """
    Regression test: NotificationConfigurations must be parsed correctly as
    List[NotificationConfiguration], not as List[NoneType] due to field name
    shadowing from the singular NotificationConfiguration field in the class body.
    """
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-123",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-123"],
                "NotificationConfigurations": [
                    {
                        "TopicARN": "arn:aws:sns:us-east-1:123456789012:launch-topic",
                        "NotificationTypes": ["autoscaling:EC2_INSTANCE_LAUNCH"],
                    },
                    {
                        "TopicARN": "arn:aws:sns:us-east-1:123456789012:terminate-topic",
                        "NotificationTypes": ["autoscaling:EC2_INSTANCE_TERMINATE"],
                    },
                ],
            },
        }
    )
    assert len(asg.Properties.NotificationConfigurations) == 2
    assert asg.Properties.NotificationConfigurations[0].TopicARN == "arn:aws:sns:us-east-1:123456789012:launch-topic"
    assert asg.Properties.NotificationConfigurations[1].TopicARN == "arn:aws:sns:us-east-1:123456789012:terminate-topic"


def test_autoscaling_group_with_tags():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-123",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-123"],
                "Tags": [
                    {"Key": "Environment", "Value": "production", "PropagateAtLaunch": True},
                    {"Key": "Application", "Value": "web", "PropagateAtLaunch": True},
                ],
            },
        }
    )
    assert len(asg.Properties.Tags) == 2
    assert asg.Properties.Tags[0].PropagateAtLaunch is True


def test_autoscaling_group_with_instance_maintenance_policy():
    asg = AutoScalingAutoScalingGroup(
        **{
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "MinSize": "1",
                "MaxSize": "5",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-123",
                    "Version": "$Latest",
                },
                "VPCZoneIdentifier": ["subnet-123"],
                "InstanceMaintenancePolicy": {
                    "MinHealthyPercentage": 90,
                    "MaxHealthyPercentage": 120,
                },
            },
        }
    )
    assert asg.Properties.InstanceMaintenancePolicy.MinHealthyPercentage == 90


def test_autoscaling_group_requires_min_size():
    with pytest.raises(ValidationError):
        AutoScalingAutoScalingGroup(
            **{
                "Type": "AWS::AutoScaling::AutoScalingGroup",
                "Properties": {
                    "MaxSize": "5",
                    "LaunchTemplate": {
                        "LaunchTemplateId": "lt-123",
                        "Version": "$Latest",
                    },
                },
            }
        )


def test_autoscaling_group_requires_max_size():
    with pytest.raises(ValidationError):
        AutoScalingAutoScalingGroup(
            **{
                "Type": "AWS::AutoScaling::AutoScalingGroup",
                "Properties": {
                    "MinSize": "1",
                    "LaunchTemplate": {
                        "LaunchTemplateId": "lt-123",
                        "Version": "$Latest",
                    },
                },
            }
        )
