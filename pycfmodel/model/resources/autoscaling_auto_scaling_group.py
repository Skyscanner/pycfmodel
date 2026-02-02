"""
AutoScalingAutoScalingGroup resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::AutoScaling::AutoScalingGroup.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableStr


class AutoScalingAutoScalingGroupProperties(CustomModel):
    """
    Properties for AWS::AutoScaling::AutoScalingGroup.

    Properties:

    - AutoScalingGroupName: The name of the Auto Scaling group. This name must be unique per Region per acco...
    - AvailabilityZoneDistribution: The EC2 instance capacity distribution across Availability Zones for the Auto Sc...
    - AvailabilityZoneImpairmentPolicy: The Availability Zone impairment policy for the Auto Scaling group.
    - AvailabilityZones: A list of Availability Zones where instances in the Auto Scaling group can be cr...
    - CapacityRebalance: Indicates whether Capacity Rebalancing is enabled. Otherwise, Capacity Rebalanci...
    - CapacityReservationSpecification: The capacity reservation specification for the Auto Scaling group.
    - Context: Reserved.
    - Cooldown: *Only needed if you use simple scaling policies.* 
 The amount of time, in secon...
    - DefaultInstanceWarmup: The amount of time, in seconds, until a new instance is considered to have finis...
    - DesiredCapacity: The desired capacity is the initial capacity of the Auto Scaling group at the ti...
    - DesiredCapacityType: The unit of measurement for the value specified for desired capacity. Amazon EC2...
    - HealthCheckGracePeriod: The amount of time, in seconds, that Amazon EC2 Auto Scaling waits before checki...
    - HealthCheckType: A comma-separated value string of one or more health check types.
 The valid val...
    - InstanceId: The ID of the instance used to base the launch configuration on. For more inform...
    - InstanceLifecyclePolicy: The instance lifecycle policy for the Auto Scaling group.
    - InstanceMaintenancePolicy: An instance maintenance policy. For more information, see [Set instance maintena...
    - LaunchConfigurationName: The name of the launch configuration to use to launch instances.
 Required only ...
    - LaunchTemplate: Information used to specify the launch template and version to use to launch ins...
    - LifecycleHookSpecificationList: One or more lifecycle hooks to add to the Auto Scaling group before instances ar...
    - LoadBalancerNames: A list of Classic Load Balancers associated with this Auto Scaling group. For Ap...
    - MaxInstanceLifetime: The maximum amount of time, in seconds, that an instance can be in service. The ...
    - MaxSize: The maximum size of the group.
  With a mixed instances policy that uses instanc...
    - MetricsCollection: Enables the monitoring of group metrics of an Auto Scaling group. By default, th...
    - MinSize: The minimum size of the group.
    - MixedInstancesPolicy: An embedded object that specifies a mixed instances policy.
 The policy includes...
    - NewInstancesProtectedFromScaleIn: Indicates whether newly launched instances are protected from termination by Ama...
    - NotificationConfiguration: 
    - NotificationConfigurations: Configures an Auto Scaling group to send notifications when specified events tak...
    - PlacementGroup: The name of the placement group into which to launch your instances. For more in...
    - ServiceLinkedRoleARN: The Amazon Resource Name (ARN) of the service-linked role that the Auto Scaling ...
    - SkipZonalShiftValidation: 
    - Tags: One or more tags. You can tag your Auto Scaling group and propagate the tags to ...
    - TargetGroupARNs: The Amazon Resource Names (ARN) of the Elastic Load Balancing target groups to a...
    - TerminationPolicies: A policy or a list of policies that are used to select the instance to terminate...
    - TrafficSources: The traffic sources associated with this Auto Scaling group.
    - VPCZoneIdentifier: A list of subnet IDs for a virtual private cloud (VPC) where instances in the Au...

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html)
    """

    MaxSize: ResolvableStr
    MinSize: ResolvableStr
    AutoScalingGroupName: Optional[ResolvableStr] = None
    AvailabilityZoneDistribution: Optional[ResolvableGeneric] = None
    AvailabilityZoneImpairmentPolicy: Optional[ResolvableGeneric] = None
    AvailabilityZones: Optional[Resolvable[List[ResolvableStr]]] = None
    CapacityRebalance: Optional[ResolvableBool] = None
    CapacityReservationSpecification: Optional[ResolvableGeneric] = None
    Context: Optional[ResolvableStr] = None
    Cooldown: Optional[ResolvableStr] = None
    DefaultInstanceWarmup: Optional[ResolvableInt] = None
    DesiredCapacity: Optional[ResolvableStr] = None
    DesiredCapacityType: Optional[ResolvableStr] = None
    HealthCheckGracePeriod: Optional[ResolvableInt] = None
    HealthCheckType: Optional[ResolvableStr] = None
    InstanceId: Optional[ResolvableStr] = None
    InstanceLifecyclePolicy: Optional[ResolvableGeneric] = None
    InstanceMaintenancePolicy: Optional[ResolvableGeneric] = None
    LaunchConfigurationName: Optional[ResolvableStr] = None
    LaunchTemplate: Optional[ResolvableGeneric] = None
    LifecycleHookSpecificationList: Optional[Resolvable[List[ResolvableGeneric]]] = None
    LoadBalancerNames: Optional[Resolvable[List[ResolvableStr]]] = None
    MaxInstanceLifetime: Optional[ResolvableInt] = None
    MetricsCollection: Optional[Resolvable[List[ResolvableGeneric]]] = None
    MixedInstancesPolicy: Optional[ResolvableGeneric] = None
    NewInstancesProtectedFromScaleIn: Optional[ResolvableBool] = None
    NotificationConfiguration: Optional[ResolvableGeneric] = None
    NotificationConfigurations: Optional[Resolvable[List[ResolvableGeneric]]] = None
    PlacementGroup: Optional[ResolvableStr] = None
    ServiceLinkedRoleARN: Optional[ResolvableStr] = None
    SkipZonalShiftValidation: Optional[ResolvableBool] = None
    Tags: Optional[Resolvable[List[ResolvableGeneric]]] = None
    TargetGroupARNs: Optional[Resolvable[List[ResolvableStr]]] = None
    TerminationPolicies: Optional[Resolvable[List[ResolvableStr]]] = None
    TrafficSources: Optional[Resolvable[List[ResolvableGeneric]]] = None
    VPCZoneIdentifier: Optional[Resolvable[List[ResolvableStr]]] = None


class AutoScalingAutoScalingGroup(Resource):
    """
    The ``AWS::AutoScaling::AutoScalingGroup`` resource defines an Amazon EC2 Auto Scaling group, which is a collection of Amazon EC2 instances that are treated as a logical grouping for the purposes of automatic scaling and management. 
 For more information about Amazon EC2 Auto Scaling, see the [Amazon EC2 Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html). 
  Amazon EC2 Auto Scaling configures instances launched as part of an Auto Scaling group using either a [launch template](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html) or a launch configuration. We strongly recommend that you do not use launch configurations. For more information, see [Launch configurations](https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-configurations.html) in the *Amazon EC2 Auto Scaling User Guide*.
 For help migrating from launch configurations to launch templates, see [Migrate CloudFormation stacks from launch configurations to launch templates](https://docs.aws.amazon.com/autoscaling/ec2/userguide/migrate-launch-configurations-with-cloudformation.html) in the *Amazon EC2 Auto Scaling User Guide*.

    Properties:

    - Properties: A [AutoScalingAutoScalingGroupProperties][pycfmodel.model.resources.autoscaling_auto_scaling_group.AutoScalingAutoScalingGroupProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html)
    """

    Type: Literal["AWS::AutoScaling::AutoScalingGroup"]
    Properties: Resolvable[AutoScalingAutoScalingGroupProperties]
