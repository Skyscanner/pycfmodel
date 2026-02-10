"""
AutoScalingAutoScalingGroup resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::AutoScaling::AutoScalingGroup.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableModel, ResolvableStr


class AcceleratorCountRequest(CustomModel):
    """
    ``AcceleratorCountRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableAcceleratorCountRequest = ResolvableModel(AcceleratorCountRequest)


class AcceleratorTotalMemoryMiBRequest(CustomModel):
    """
    ``AcceleratorTotalMemoryMiBRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableAcceleratorTotalMemoryMiBRequest = ResolvableModel(AcceleratorTotalMemoryMiBRequest)


class AvailabilityZoneDistribution(CustomModel):
    """
    ``AvailabilityZoneDistribution`` is a property of the [AWS::AutoScaling::AutoScalingGroup](https://docs.
    """

    CapacityDistributionStrategy: Optional[ResolvableStr] = None


ResolvableAvailabilityZoneDistribution = ResolvableModel(AvailabilityZoneDistribution)


class AvailabilityZoneImpairmentPolicy(CustomModel):
    """
    Describes an Availability Zone impairment policy.
    """

    ImpairedZoneHealthCheckBehavior: ResolvableStr
    ZonalShiftEnabled: ResolvableBool


ResolvableAvailabilityZoneImpairmentPolicy = ResolvableModel(AvailabilityZoneImpairmentPolicy)


class BaselineEbsBandwidthMbpsRequest(CustomModel):
    """
    ``BaselineEbsBandwidthMbpsRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableBaselineEbsBandwidthMbpsRequest = ResolvableModel(BaselineEbsBandwidthMbpsRequest)


class CapacityReservationTarget(CustomModel):
    """
    The target for the Capacity Reservation.
    """

    CapacityReservationIds: Optional[Resolvable[List[ResolvableStr]]] = None
    CapacityReservationResourceGroupArns: Optional[Resolvable[List[ResolvableStr]]] = None


ResolvableCapacityReservationTarget = ResolvableModel(CapacityReservationTarget)


class CapacityReservationSpecification(CustomModel):
    """
    Describes the Capacity Reservation preference and targeting options.
    """

    CapacityReservationPreference: ResolvableStr
    CapacityReservationTarget: Optional[ResolvableCapacityReservationTarget] = None


ResolvableCapacityReservationSpecification = ResolvableModel(CapacityReservationSpecification)


class InstanceMaintenancePolicy(CustomModel):
    """
    ``InstanceMaintenancePolicy`` is a property of the [AWS::AutoScaling::AutoScalingGroup](https://docs.
    """

    MaxHealthyPercentage: Optional[ResolvableInt] = None
    MinHealthyPercentage: Optional[ResolvableInt] = None


ResolvableInstanceMaintenancePolicy = ResolvableModel(InstanceMaintenancePolicy)


class InstancesDistribution(CustomModel):
    """
    Use this structure to specify the distribution of On-Demand Instances and Spot Instances and the allocation strategies used to fulfill On-Demand and Spot capacities for a mixed instances policy.
    """

    OnDemandAllocationStrategy: Optional[ResolvableStr] = None
    OnDemandBaseCapacity: Optional[ResolvableInt] = None
    OnDemandPercentageAboveBaseCapacity: Optional[ResolvableInt] = None
    SpotAllocationStrategy: Optional[ResolvableStr] = None
    SpotInstancePools: Optional[ResolvableInt] = None
    SpotMaxPrice: Optional[ResolvableStr] = None


ResolvableInstancesDistribution = ResolvableModel(InstancesDistribution)


class LaunchTemplateSpecification(CustomModel):
    """
    Specifies a launch template to use when provisioning EC2 instances for an Auto Scaling group.
    """

    Version: ResolvableStr
    LaunchTemplateId: Optional[ResolvableStr] = None
    LaunchTemplateName: Optional[ResolvableStr] = None


ResolvableLaunchTemplateSpecification = ResolvableModel(LaunchTemplateSpecification)


class LifecycleHookSpecification(CustomModel):
    """
    ``LifecycleHookSpecification`` specifies a lifecycle hook for the ``LifecycleHookSpecificationList`` property of the [AWS::AutoScaling::AutoScalingGroup](https://docs.
    """

    LifecycleHookName: ResolvableStr
    LifecycleTransition: ResolvableStr
    DefaultResult: Optional[ResolvableStr] = None
    HeartbeatTimeout: Optional[ResolvableInt] = None
    NotificationMetadata: Optional[ResolvableStr] = None
    NotificationTargetARN: Optional[ResolvableStr] = None
    RoleARN: Optional[ResolvableStr] = None


ResolvableLifecycleHookSpecification = ResolvableModel(LifecycleHookSpecification)


class MemoryGiBPerVCpuRequest(CustomModel):
    """
    ``MemoryGiBPerVCpuRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableMemoryGiBPerVCpuRequest = ResolvableModel(MemoryGiBPerVCpuRequest)


class MemoryMiBRequest(CustomModel):
    """
    ``MemoryMiBRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableMemoryMiBRequest = ResolvableModel(MemoryMiBRequest)


class MetricsCollection(CustomModel):
    """
    ``MetricsCollection`` is a property of the [AWS::AutoScaling::AutoScalingGroup](https://docs.
    """

    Granularity: ResolvableStr
    Metrics: Optional[Resolvable[List[ResolvableStr]]] = None


ResolvableMetricsCollection = ResolvableModel(MetricsCollection)


class NetworkBandwidthGbpsRequest(CustomModel):
    """
    ``NetworkBandwidthGbpsRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableNetworkBandwidthGbpsRequest = ResolvableModel(NetworkBandwidthGbpsRequest)


class NetworkInterfaceCountRequest(CustomModel):
    """
    ``NetworkInterfaceCountRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableNetworkInterfaceCountRequest = ResolvableModel(NetworkInterfaceCountRequest)


class NotificationConfiguration(CustomModel):
    """
    A structure that specifies an Amazon SNS notification configuration for the ``NotificationConfigurations`` property of the [AWS::AutoScaling::AutoScalingGroup](https://docs.
    """

    TopicARN: ResolvableStr
    NotificationTypes: Optional[Resolvable[List[ResolvableStr]]] = None


ResolvableNotificationConfiguration = ResolvableModel(NotificationConfiguration)


class PerformanceFactorReferenceRequest(CustomModel):
    """
    Specify an instance family to use as the baseline reference for CPU performance.
    """

    InstanceFamily: Optional[ResolvableStr] = None


ResolvablePerformanceFactorReferenceRequest = ResolvableModel(PerformanceFactorReferenceRequest)


class CpuPerformanceFactorRequest(CustomModel):
    """
    The CPU performance to consider, using an instance family as the baseline reference.
    """

    References: Optional[Resolvable[List[PerformanceFactorReferenceRequest]]] = None


ResolvableCpuPerformanceFactorRequest = ResolvableModel(CpuPerformanceFactorRequest)


class BaselinePerformanceFactorsRequest(CustomModel):
    """
    The baseline performance to consider, using an instance family as a baseline reference.
    """

    Cpu: Optional[ResolvableCpuPerformanceFactorRequest] = None


ResolvableBaselinePerformanceFactorsRequest = ResolvableModel(BaselinePerformanceFactorsRequest)


class RetentionTriggers(CustomModel):
    """
    Defines the specific triggers that cause instances to be retained in a Retained state rather than terminated.
    """

    TerminateHookAbandon: Optional[ResolvableStr] = None


ResolvableRetentionTriggers = ResolvableModel(RetentionTriggers)


class InstanceLifecyclePolicy(CustomModel):
    """
    The instance lifecycle policy for the Auto Scaling group.
    """

    RetentionTriggers: Optional[ResolvableRetentionTriggers] = None


ResolvableInstanceLifecyclePolicy = ResolvableModel(InstanceLifecyclePolicy)


class TagProperty(CustomModel):
    """
    A structure that specifies a tag for the ``Tags`` property of [AWS::AutoScaling::AutoScalingGroup](https://docs.
    """

    Key: ResolvableStr
    PropagateAtLaunch: ResolvableBool
    Value: ResolvableStr


ResolvableTagProperty = ResolvableModel(TagProperty)


class TotalLocalStorageGBRequest(CustomModel):
    """
    ``TotalLocalStorageGBRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableTotalLocalStorageGBRequest = ResolvableModel(TotalLocalStorageGBRequest)


class TrafficSourceIdentifier(CustomModel):
    """
    Identifying information for a traffic source.
    """

    Identifier: ResolvableStr
    Type: ResolvableStr


ResolvableTrafficSourceIdentifier = ResolvableModel(TrafficSourceIdentifier)


class VCpuCountRequest(CustomModel):
    """
    ``VCpuCountRequest`` is a property of the ``InstanceRequirements`` property of the [AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides](https://docs.
    """

    Max: Optional[ResolvableInt] = None
    Min: Optional[ResolvableInt] = None


ResolvableVCpuCountRequest = ResolvableModel(VCpuCountRequest)


class InstanceRequirements(CustomModel):
    """
    The attributes for the instance types for a mixed instances policy.
    """

    MemoryMiB: ResolvableMemoryMiBRequest
    VCpuCount: ResolvableVCpuCountRequest
    AcceleratorCount: Optional[ResolvableAcceleratorCountRequest] = None
    AcceleratorManufacturers: Optional[Resolvable[List[ResolvableStr]]] = None
    AcceleratorNames: Optional[Resolvable[List[ResolvableStr]]] = None
    AcceleratorTotalMemoryMiB: Optional[ResolvableAcceleratorTotalMemoryMiBRequest] = None
    AcceleratorTypes: Optional[Resolvable[List[ResolvableStr]]] = None
    AllowedInstanceTypes: Optional[Resolvable[List[ResolvableStr]]] = None
    BareMetal: Optional[ResolvableStr] = None
    BaselineEbsBandwidthMbps: Optional[ResolvableBaselineEbsBandwidthMbpsRequest] = None
    BaselinePerformanceFactors: Optional[ResolvableBaselinePerformanceFactorsRequest] = None
    BurstablePerformance: Optional[ResolvableStr] = None
    CpuManufacturers: Optional[Resolvable[List[ResolvableStr]]] = None
    ExcludedInstanceTypes: Optional[Resolvable[List[ResolvableStr]]] = None
    InstanceGenerations: Optional[Resolvable[List[ResolvableStr]]] = None
    LocalStorage: Optional[ResolvableStr] = None
    LocalStorageTypes: Optional[Resolvable[List[ResolvableStr]]] = None
    MaxSpotPriceAsPercentageOfOptimalOnDemandPrice: Optional[ResolvableInt] = None
    MemoryGiBPerVCpu: Optional[ResolvableMemoryGiBPerVCpuRequest] = None
    NetworkBandwidthGbps: Optional[ResolvableNetworkBandwidthGbpsRequest] = None
    NetworkInterfaceCount: Optional[ResolvableNetworkInterfaceCountRequest] = None
    OnDemandMaxPricePercentageOverLowestPrice: Optional[ResolvableInt] = None
    RequireHibernateSupport: Optional[ResolvableBool] = None
    SpotMaxPricePercentageOverLowestPrice: Optional[ResolvableInt] = None
    TotalLocalStorageGB: Optional[ResolvableTotalLocalStorageGBRequest] = None


ResolvableInstanceRequirements = ResolvableModel(InstanceRequirements)


class LaunchTemplateOverrides(CustomModel):
    """
      Use this structure to let Amazon EC2 Auto Scaling do the following when the Auto Scaling group has a mixed instances policy:
    +  Override the instance type that is specified in the launch template.
    """

    ImageId: Optional[ResolvableStr] = None
    InstanceRequirements: Optional[ResolvableInstanceRequirements] = None
    InstanceType: Optional[ResolvableStr] = None
    LaunchTemplateSpecification: Optional[ResolvableLaunchTemplateSpecification] = None
    WeightedCapacity: Optional[ResolvableStr] = None


ResolvableLaunchTemplateOverrides = ResolvableModel(LaunchTemplateOverrides)


class LaunchTemplate(CustomModel):
    """
    Use this structure to specify the launch templates and instance types (overrides) for a mixed instances policy.
    """

    LaunchTemplateSpecification: ResolvableLaunchTemplateSpecification
    Overrides: Optional[Resolvable[List[LaunchTemplateOverrides]]] = None


ResolvableLaunchTemplate = ResolvableModel(LaunchTemplate)


class MixedInstancesPolicy(CustomModel):
    """
    Use this structure to launch multiple instance types and On-Demand Instances and Spot Instances within a single Auto Scaling group.
    """

    LaunchTemplate: ResolvableLaunchTemplate
    InstancesDistribution: Optional[ResolvableInstancesDistribution] = None


ResolvableMixedInstancesPolicy = ResolvableModel(MixedInstancesPolicy)


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
    AvailabilityZoneDistribution: Optional[ResolvableAvailabilityZoneDistribution] = None
    AvailabilityZoneImpairmentPolicy: Optional[ResolvableAvailabilityZoneImpairmentPolicy] = None
    AvailabilityZones: Optional[Resolvable[List[ResolvableStr]]] = None
    CapacityRebalance: Optional[ResolvableBool] = None
    CapacityReservationSpecification: Optional[ResolvableCapacityReservationSpecification] = None
    Context: Optional[ResolvableStr] = None
    Cooldown: Optional[ResolvableStr] = None
    DefaultInstanceWarmup: Optional[ResolvableInt] = None
    DesiredCapacity: Optional[ResolvableStr] = None
    DesiredCapacityType: Optional[ResolvableStr] = None
    HealthCheckGracePeriod: Optional[ResolvableInt] = None
    HealthCheckType: Optional[ResolvableStr] = None
    InstanceId: Optional[ResolvableStr] = None
    InstanceLifecyclePolicy: Optional[ResolvableInstanceLifecyclePolicy] = None
    InstanceMaintenancePolicy: Optional[ResolvableInstanceMaintenancePolicy] = None
    LaunchConfigurationName: Optional[ResolvableStr] = None
    LaunchTemplate: Optional[ResolvableLaunchTemplateSpecification] = None
    LifecycleHookSpecificationList: Optional[Resolvable[List[LifecycleHookSpecification]]] = None
    LoadBalancerNames: Optional[Resolvable[List[ResolvableStr]]] = None
    MaxInstanceLifetime: Optional[ResolvableInt] = None
    MetricsCollection: Optional[Resolvable[List[MetricsCollection]]] = None
    MixedInstancesPolicy: Optional[ResolvableMixedInstancesPolicy] = None
    NewInstancesProtectedFromScaleIn: Optional[ResolvableBool] = None
    NotificationConfiguration: Optional[ResolvableNotificationConfiguration] = None
    NotificationConfigurations: Optional[Resolvable[List[NotificationConfiguration]]] = None
    PlacementGroup: Optional[ResolvableStr] = None
    ServiceLinkedRoleARN: Optional[ResolvableStr] = None
    SkipZonalShiftValidation: Optional[ResolvableBool] = None
    Tags: Optional[Resolvable[List[TagProperty]]] = None
    TargetGroupARNs: Optional[Resolvable[List[ResolvableStr]]] = None
    TerminationPolicies: Optional[Resolvable[List[ResolvableStr]]] = None
    TrafficSources: Optional[Resolvable[List[TrafficSourceIdentifier]]] = None
    VPCZoneIdentifier: Optional[Resolvable[List[ResolvableStr]]] = None


class AutoScalingAutoScalingGroup(Resource):
    """
    The ``AWS::AutoScaling::AutoScalingGroup`` resource defines an Amazon EC2 Auto Scaling group, which is a collection of Amazon EC2 instances that are treated as a logical grouping for the purposes of a

    Properties:

    - Properties: A [AutoScalingAutoScalingGroupProperties][pycfmodel.model.resources.autoscaling_auto_scaling_group.AutoScalingAutoScalingGroupProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html)
    """

    Type: Literal["AWS::AutoScaling::AutoScalingGroup"]
    Properties: Resolvable[AutoScalingAutoScalingGroupProperties]
