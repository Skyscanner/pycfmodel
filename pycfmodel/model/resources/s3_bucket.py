"""
S3Bucket resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::S3::Bucket.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableModel, ResolvableStr


class AbortIncompleteMultipartUpload(CustomModel):
    """
    Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 will wait before permanently removing all parts of the upload.
    """

    DaysAfterInitiation: ResolvableInt


ResolvableAbortIncompleteMultipartUpload = ResolvableModel(AbortIncompleteMultipartUpload)


class AccelerateConfiguration(CustomModel):
    """
    Configures the transfer acceleration state for an Amazon S3 bucket.
    """

    AccelerationStatus: ResolvableStr


ResolvableAccelerateConfiguration = ResolvableModel(AccelerateConfiguration)


class AccessControlTranslation(CustomModel):
    """
    Specify this only in a cross-account scenario (where source and destination bucket owners are not the same), and you want to change replica ownership to the AWS-account that owns the destination bucket.
    """

    Owner: ResolvableStr


ResolvableAccessControlTranslation = ResolvableModel(AccessControlTranslation)


class BlockedEncryptionTypes(CustomModel):
    """
    A bucket-level setting for Amazon S3 general purpose buckets used to prevent the upload of new objects encrypted with the specified server-side encryption type.
    """

    EncryptionType: Optional[Resolvable[List[ResolvableStr]]] = None


ResolvableBlockedEncryptionTypes = ResolvableModel(BlockedEncryptionTypes)


class CorsRule(CustomModel):
    """
    Specifies a cross-origin access rule for an Amazon S3 bucket.
    """

    AllowedMethods: Resolvable[List[ResolvableStr]]
    AllowedOrigins: Resolvable[List[ResolvableStr]]
    AllowedHeaders: Optional[Resolvable[List[ResolvableStr]]] = None
    ExposedHeaders: Optional[Resolvable[List[ResolvableStr]]] = None
    Id: Optional[ResolvableStr] = None
    MaxAge: Optional[ResolvableInt] = None


ResolvableCorsRule = ResolvableModel(CorsRule)


class CorsConfiguration(CustomModel):
    """
    Describes the cross-origin access configuration for objects in an Amazon S3 bucket.
    """

    CorsRules: Resolvable[List[CorsRule]]


ResolvableCorsConfiguration = ResolvableModel(CorsConfiguration)


class DefaultRetention(CustomModel):
    """
    The container element for optionally specifying the default Object Lock retention settings for new objects placed in the specified bucket.
    """

    Days: Optional[ResolvableInt] = None
    Mode: Optional[ResolvableStr] = None
    Years: Optional[ResolvableInt] = None


ResolvableDefaultRetention = ResolvableModel(DefaultRetention)


class DeleteMarkerReplication(CustomModel):
    """
    Specifies whether Amazon S3 replicates delete markers.
    """

    Status: Optional[ResolvableStr] = None


ResolvableDeleteMarkerReplication = ResolvableModel(DeleteMarkerReplication)


class Destination(CustomModel):
    """
    Specifies information about where to publish analysis or configuration results for an Amazon S3 bucket.
    """

    BucketArn: ResolvableStr
    Format: ResolvableStr
    BucketAccountId: Optional[ResolvableStr] = None
    Prefix: Optional[ResolvableStr] = None


ResolvableDestination = ResolvableModel(Destination)


class DataExport(CustomModel):
    """
    Specifies how data related to the storage class analysis for an Amazon S3 bucket should be exported.
    """

    Destination: ResolvableDestination
    OutputSchemaVersion: ResolvableStr


ResolvableDataExport = ResolvableModel(DataExport)


class EncryptionConfiguration(CustomModel):
    """
    Specifies encryption-related information for an Amazon S3 bucket that is a destination for replicated objects.
    """

    ReplicaKmsKeyID: ResolvableStr


ResolvableEncryptionConfiguration = ResolvableModel(EncryptionConfiguration)


class EventBridgeConfiguration(CustomModel):
    """
    Amazon S3 can send events to Amazon EventBridge whenever certain events happen in your bucket, see [Using EventBridge](https://docs.
    """

    EventBridgeEnabled: ResolvableBool


ResolvableEventBridgeConfiguration = ResolvableModel(EventBridgeConfiguration)


class FilterRule(CustomModel):
    """
    Specifies the Amazon S3 object key name to filter on.
    """

    Name: ResolvableStr
    Value: ResolvableStr


ResolvableFilterRule = ResolvableModel(FilterRule)


class InventoryConfiguration(CustomModel):
    """
    Specifies the S3 Inventory configuration for an Amazon S3 bucket.
    """

    Destination: ResolvableDestination
    Enabled: ResolvableBool
    Id: ResolvableStr
    IncludedObjectVersions: ResolvableStr
    ScheduleFrequency: ResolvableStr
    OptionalFields: Optional[Resolvable[List[ResolvableStr]]] = None
    Prefix: Optional[ResolvableStr] = None


ResolvableInventoryConfiguration = ResolvableModel(InventoryConfiguration)


class MetadataDestination(CustomModel):
    """
    The destination information for the S3 Metadata configuration.
    """

    TableBucketType: ResolvableStr
    TableBucketArn: Optional[ResolvableStr] = None
    TableNamespace: Optional[ResolvableStr] = None


ResolvableMetadataDestination = ResolvableModel(MetadataDestination)


class MetadataTableEncryptionConfiguration(CustomModel):
    """
    The encryption settings for an S3 Metadata journal table or inventory table configuration.
    """

    SseAlgorithm: ResolvableStr
    KmsKeyArn: Optional[ResolvableStr] = None


ResolvableMetadataTableEncryptionConfiguration = ResolvableModel(MetadataTableEncryptionConfiguration)


class InventoryTableConfiguration(CustomModel):
    """
    The inventory table configuration for an S3 Metadata configuration.
    """

    ConfigurationState: ResolvableStr
    EncryptionConfiguration: Optional[ResolvableMetadataTableEncryptionConfiguration] = None
    TableArn: Optional[ResolvableStr] = None
    TableName: Optional[ResolvableStr] = None


ResolvableInventoryTableConfiguration = ResolvableModel(InventoryTableConfiguration)


class NoncurrentVersionExpiration(CustomModel):
    """
    Specifies when noncurrent object versions expire.
    """

    NoncurrentDays: ResolvableInt
    NewerNoncurrentVersions: Optional[ResolvableInt] = None


ResolvableNoncurrentVersionExpiration = ResolvableModel(NoncurrentVersionExpiration)


class NoncurrentVersionTransition(CustomModel):
    """
    Container for the transition rule that describes when noncurrent objects transition to the ``STANDARD_IA``, ``ONEZONE_IA``, ``INTELLIGENT_TIERING``, ``GLACIER_IR``, ``GLACIER``, or ``DEEP_ARCHIVE`` storage class.
    """

    StorageClass: ResolvableStr
    TransitionInDays: ResolvableInt
    NewerNoncurrentVersions: Optional[ResolvableInt] = None


ResolvableNoncurrentVersionTransition = ResolvableModel(NoncurrentVersionTransition)


class ObjectLockRule(CustomModel):
    """
    Specifies the Object Lock rule for the specified object.
    """

    DefaultRetention: Optional[ResolvableDefaultRetention] = None


ResolvableObjectLockRule = ResolvableModel(ObjectLockRule)


class ObjectLockConfiguration(CustomModel):
    """
    Places an Object Lock configuration on the specified bucket.
    """

    ObjectLockEnabled: Optional[ResolvableStr] = None
    Rule: Optional[ResolvableObjectLockRule] = None


ResolvableObjectLockConfiguration = ResolvableModel(ObjectLockConfiguration)


class OwnershipControlsRule(CustomModel):
    """
    Specifies an Object Ownership rule.
    """

    ObjectOwnership: Optional[ResolvableStr] = None


ResolvableOwnershipControlsRule = ResolvableModel(OwnershipControlsRule)


class OwnershipControls(CustomModel):
    """
    Specifies the container element for Object Ownership rules.
    """

    Rules: Resolvable[List[OwnershipControlsRule]]


ResolvableOwnershipControls = ResolvableModel(OwnershipControls)


class PublicAccessBlockConfiguration(CustomModel):
    """
    The PublicAccessBlock configuration that you want to apply to this Amazon S3 bucket.
    """

    BlockPublicAcls: Optional[ResolvableBool] = None
    BlockPublicPolicy: Optional[ResolvableBool] = None
    IgnorePublicAcls: Optional[ResolvableBool] = None
    RestrictPublicBuckets: Optional[ResolvableBool] = None


ResolvablePublicAccessBlockConfiguration = ResolvableModel(PublicAccessBlockConfiguration)


class RecordExpiration(CustomModel):
    """
    The journal table record expiration settings for a journal table in an S3 Metadata configuration.
    """

    Expiration: ResolvableStr
    Days: Optional[ResolvableInt] = None


ResolvableRecordExpiration = ResolvableModel(RecordExpiration)


class JournalTableConfiguration(CustomModel):
    """
    The journal table configuration for an S3 Metadata configuration.
    """

    RecordExpiration: ResolvableRecordExpiration
    EncryptionConfiguration: Optional[ResolvableMetadataTableEncryptionConfiguration] = None
    TableArn: Optional[ResolvableStr] = None
    TableName: Optional[ResolvableStr] = None


ResolvableJournalTableConfiguration = ResolvableModel(JournalTableConfiguration)


class MetadataConfiguration(CustomModel):
    """
    Creates a V2 S3 Metadata configuration of a general purpose bucket.
    """

    JournalTableConfiguration: ResolvableJournalTableConfiguration
    Destination: Optional[ResolvableMetadataDestination] = None
    InventoryTableConfiguration: Optional[ResolvableInventoryTableConfiguration] = None


ResolvableMetadataConfiguration = ResolvableModel(MetadataConfiguration)


class RedirectAllRequestsTo(CustomModel):
    """
    Specifies the redirect behavior of all requests to a website endpoint of an Amazon S3 bucket.
    """

    HostName: ResolvableStr
    Protocol: Optional[ResolvableStr] = None


ResolvableRedirectAllRequestsTo = ResolvableModel(RedirectAllRequestsTo)


class RedirectRule(CustomModel):
    """
    Specifies how requests are redirected.
    """

    HostName: Optional[ResolvableStr] = None
    HttpRedirectCode: Optional[ResolvableStr] = None
    Protocol: Optional[ResolvableStr] = None
    ReplaceKeyPrefixWith: Optional[ResolvableStr] = None
    ReplaceKeyWith: Optional[ResolvableStr] = None


ResolvableRedirectRule = ResolvableModel(RedirectRule)


class ReplicaModifications(CustomModel):
    """
    A filter that you can specify for selection for modifications on replicas.
    """

    Status: ResolvableStr


ResolvableReplicaModifications = ResolvableModel(ReplicaModifications)


class ReplicationTimeValue(CustomModel):
    """
    A container specifying the time value for S3 Replication Time Control (S3 RTC) and replication metrics ``EventThreshold``.
    """

    Minutes: ResolvableInt


ResolvableReplicationTimeValue = ResolvableModel(ReplicationTimeValue)


class Metrics(CustomModel):
    """
    A container specifying replication metrics-related settings enabling replication metrics and events.
    """

    Status: ResolvableStr
    EventThreshold: Optional[ResolvableReplicationTimeValue] = None


ResolvableMetrics = ResolvableModel(Metrics)


class ReplicationTime(CustomModel):
    """
    A container specifying S3 Replication Time Control (S3 RTC) related information, including whether S3 RTC is enabled and the time when all objects and operations on objects must be replicated.
    """

    Status: ResolvableStr
    Time: ResolvableReplicationTimeValue


ResolvableReplicationTime = ResolvableModel(ReplicationTime)


class ReplicationDestination(CustomModel):
    """
    A container for information about the replication destination and its configurations including enabling the S3 Replication Time Control (S3 RTC).
    """

    Bucket: ResolvableStr
    AccessControlTranslation: Optional[ResolvableAccessControlTranslation] = None
    Account: Optional[ResolvableStr] = None
    EncryptionConfiguration: Optional[ResolvableEncryptionConfiguration] = None
    Metrics: Optional[ResolvableMetrics] = None
    ReplicationTime: Optional[ResolvableReplicationTime] = None
    StorageClass: Optional[ResolvableStr] = None


ResolvableReplicationDestination = ResolvableModel(ReplicationDestination)


class RoutingRuleCondition(CustomModel):
    """
    A container for describing a condition that must be met for the specified redirect to apply.
    """

    HttpErrorCodeReturnedEquals: Optional[ResolvableStr] = None
    KeyPrefixEquals: Optional[ResolvableStr] = None


ResolvableRoutingRuleCondition = ResolvableModel(RoutingRuleCondition)


class RoutingRule(CustomModel):
    """
    Specifies the redirect behavior and when a redirect is applied.
    """

    RedirectRule: ResolvableRedirectRule
    RoutingRuleCondition: Optional[ResolvableRoutingRuleCondition] = None


ResolvableRoutingRule = ResolvableModel(RoutingRule)


class S3KeyFilter(CustomModel):
    """
    A container for object key name prefix and suffix filtering rules.
    """

    Rules: Resolvable[List[FilterRule]]


ResolvableS3KeyFilter = ResolvableModel(S3KeyFilter)


class NotificationFilter(CustomModel):
    """
    Specifies object key name filtering rules.
    """

    S3Key: ResolvableS3KeyFilter


ResolvableNotificationFilter = ResolvableModel(NotificationFilter)


class LambdaConfiguration(CustomModel):
    """
    Describes the LAMlong functions to invoke and the events for which to invoke them.
    """

    Event: ResolvableStr
    Function: ResolvableStr
    Filter: Optional[ResolvableNotificationFilter] = None


ResolvableLambdaConfiguration = ResolvableModel(LambdaConfiguration)


class QueueConfiguration(CustomModel):
    """
    Specifies the configuration for publishing messages to an Amazon Simple Queue Service (Amazon SQS) queue when Amazon S3 detects specified events.
    """

    Event: ResolvableStr
    Queue: ResolvableStr
    Filter: Optional[ResolvableNotificationFilter] = None


ResolvableQueueConfiguration = ResolvableModel(QueueConfiguration)


class S3TablesDestination(CustomModel):
    """
    The destination information for a V1 S3 Metadata configuration.
    """

    TableBucketArn: ResolvableStr
    TableName: ResolvableStr
    TableArn: Optional[ResolvableStr] = None
    TableNamespace: Optional[ResolvableStr] = None


ResolvableS3TablesDestination = ResolvableModel(S3TablesDestination)


class MetadataTableConfiguration(CustomModel):
    """
    We recommend that you create your S3 Metadata configurations by using the V2 [MetadataConfiguration](https://docs.
    """

    S3TablesDestination: ResolvableS3TablesDestination


ResolvableMetadataTableConfiguration = ResolvableModel(MetadataTableConfiguration)


class ServerSideEncryptionByDefault(CustomModel):
    """
    Describes the default server-side encryption to apply to new objects in the bucket.
    """

    SSEAlgorithm: ResolvableStr
    KMSMasterKeyID: Optional[ResolvableStr] = None


ResolvableServerSideEncryptionByDefault = ResolvableModel(ServerSideEncryptionByDefault)


class ServerSideEncryptionRule(CustomModel):
    """
    Specifies the default server-side encryption configuration.
    """

    BlockedEncryptionTypes: Optional[ResolvableBlockedEncryptionTypes] = None
    BucketKeyEnabled: Optional[ResolvableBool] = None
    ServerSideEncryptionByDefault: Optional[ResolvableServerSideEncryptionByDefault] = None


ResolvableServerSideEncryptionRule = ResolvableModel(ServerSideEncryptionRule)


class BucketEncryption(CustomModel):
    """
    Specifies default encryption for a bucket using server-side encryption with Amazon S3-managed keys (SSE-S3), AWS KMS-managed keys (SSE-KMS), or dual-layer server-side encryption with KMS-managed keys (DSSE-KMS).
    """

    ServerSideEncryptionConfiguration: Resolvable[List[ServerSideEncryptionRule]]


ResolvableBucketEncryption = ResolvableModel(BucketEncryption)


class SseKmsEncryptedObjects(CustomModel):
    """
    A container for filter information for the selection of S3 objects encrypted with AWS KMS.
    """

    Status: ResolvableStr


ResolvableSseKmsEncryptedObjects = ResolvableModel(SseKmsEncryptedObjects)


class SourceSelectionCriteria(CustomModel):
    """
    A container that describes additional filters for identifying the source objects that you want to replicate.
    """

    ReplicaModifications: Optional[ResolvableReplicaModifications] = None
    SseKmsEncryptedObjects: Optional[ResolvableSseKmsEncryptedObjects] = None


ResolvableSourceSelectionCriteria = ResolvableModel(SourceSelectionCriteria)


class StorageClassAnalysis(CustomModel):
    """
    Specifies data related to access patterns to be collected and made available to analyze the tradeoffs between different storage classes for an Amazon S3 bucket.
    """

    DataExport: Optional[ResolvableDataExport] = None


ResolvableStorageClassAnalysis = ResolvableModel(StorageClassAnalysis)


class TagFilter(CustomModel):
    """
    Specifies tags to use to identify a subset of objects for an Amazon S3 bucket.
    """

    Key: ResolvableStr
    Value: ResolvableStr


ResolvableTagFilter = ResolvableModel(TagFilter)


class AnalyticsConfiguration(CustomModel):
    """
    Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.
    """

    Id: ResolvableStr
    StorageClassAnalysis: ResolvableStorageClassAnalysis
    Prefix: Optional[ResolvableStr] = None
    TagFilters: Optional[Resolvable[List[TagFilter]]] = None


ResolvableAnalyticsConfiguration = ResolvableModel(AnalyticsConfiguration)


class MetricsConfiguration(CustomModel):
    """
    Specifies a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from an Amazon S3 bucket.
    """

    Id: ResolvableStr
    AccessPointArn: Optional[ResolvableStr] = None
    Prefix: Optional[ResolvableStr] = None
    TagFilters: Optional[Resolvable[List[TagFilter]]] = None


ResolvableMetricsConfiguration = ResolvableModel(MetricsConfiguration)


class ReplicationRuleAndOperator(CustomModel):
    """
    A container for specifying rule filters.
    """

    Prefix: Optional[ResolvableStr] = None
    TagFilters: Optional[Resolvable[List[TagFilter]]] = None


ResolvableReplicationRuleAndOperator = ResolvableModel(ReplicationRuleAndOperator)


class ReplicationRuleFilter(CustomModel):
    """
    A filter that identifies the subset of objects to which the replication rule applies.
    """

    And: Optional[ResolvableReplicationRuleAndOperator] = None
    Prefix: Optional[ResolvableStr] = None
    TagFilter: Optional[ResolvableTagFilter] = None


ResolvableReplicationRuleFilter = ResolvableModel(ReplicationRuleFilter)


class ReplicationRule(CustomModel):
    """
    Specifies which Amazon S3 objects to replicate and where to store the replicas.
    """

    Destination: ResolvableReplicationDestination
    Status: ResolvableStr
    DeleteMarkerReplication: Optional[ResolvableDeleteMarkerReplication] = None
    Filter: Optional[ResolvableReplicationRuleFilter] = None
    Id: Optional[ResolvableStr] = None
    Prefix: Optional[ResolvableStr] = None
    Priority: Optional[ResolvableInt] = None
    SourceSelectionCriteria: Optional[ResolvableSourceSelectionCriteria] = None


ResolvableReplicationRule = ResolvableModel(ReplicationRule)


class ReplicationConfiguration(CustomModel):
    """
    A container for replication rules.
    """

    Role: ResolvableStr
    Rules: Resolvable[List[ReplicationRule]]


ResolvableReplicationConfiguration = ResolvableModel(ReplicationConfiguration)


class TargetObjectKeyFormat(CustomModel):
    """
    Describes the key format for server access log file in the target bucket.
    """

    pass


ResolvableTargetObjectKeyFormat = ResolvableModel(TargetObjectKeyFormat)


class LoggingConfiguration(CustomModel):
    """
    Describes where logs are stored and the prefix that Amazon S3 assigns to all log object keys for a bucket.
    """

    DestinationBucketName: Optional[ResolvableStr] = None
    LogFilePrefix: Optional[ResolvableStr] = None
    TargetObjectKeyFormat: Optional[ResolvableTargetObjectKeyFormat] = None


ResolvableLoggingConfiguration = ResolvableModel(LoggingConfiguration)


class Tiering(CustomModel):
    """
    The S3 Intelligent-Tiering storage class is designed to optimize storage costs by automatically moving data to the most cost-effective storage access tier, without additional operational overhead.
    """

    AccessTier: ResolvableStr
    Days: ResolvableInt


ResolvableTiering = ResolvableModel(Tiering)


class IntelligentTieringConfiguration(CustomModel):
    """
    Specifies the S3 Intelligent-Tiering configuration for an Amazon S3 bucket.
    """

    Id: ResolvableStr
    Status: ResolvableStr
    Tierings: Resolvable[List[Tiering]]
    Prefix: Optional[ResolvableStr] = None
    TagFilters: Optional[Resolvable[List[TagFilter]]] = None


ResolvableIntelligentTieringConfiguration = ResolvableModel(IntelligentTieringConfiguration)


class TopicConfiguration(CustomModel):
    """
    A container for specifying the configuration for publication of messages to an Amazon Simple Notification Service (Amazon SNS) topic when Amazon S3 detects specified events.
    """

    Event: ResolvableStr
    Topic: ResolvableStr
    Filter: Optional[ResolvableNotificationFilter] = None


ResolvableTopicConfiguration = ResolvableModel(TopicConfiguration)


class NotificationConfiguration(CustomModel):
    """
    Describes the notification configuration for an Amazon S3 bucket.
    """

    EventBridgeConfiguration: Optional[ResolvableEventBridgeConfiguration] = None
    LambdaConfigurations: Optional[Resolvable[List[LambdaConfiguration]]] = None
    QueueConfigurations: Optional[Resolvable[List[QueueConfiguration]]] = None
    TopicConfigurations: Optional[Resolvable[List[TopicConfiguration]]] = None


ResolvableNotificationConfiguration = ResolvableModel(NotificationConfiguration)


class VersioningConfiguration(CustomModel):
    """
    Describes the versioning state of an Amazon S3 bucket.
    """

    Status: ResolvableStr


ResolvableVersioningConfiguration = ResolvableModel(VersioningConfiguration)


class WebsiteConfiguration(CustomModel):
    """
    Specifies website configuration parameters for an Amazon S3 bucket.
    """

    ErrorDocument: Optional[ResolvableStr] = None
    IndexDocument: Optional[ResolvableStr] = None
    RedirectAllRequestsTo: Optional[ResolvableRedirectAllRequestsTo] = None
    RoutingRules: Optional[Resolvable[List[RoutingRule]]] = None


ResolvableWebsiteConfiguration = ResolvableModel(WebsiteConfiguration)


class Transition(CustomModel):
    """
    Specifies when an object transitions to a specified storage class.
    """

    StorageClass: ResolvableStr
    TransitionDate: Optional[ResolvableStr] = None
    TransitionInDays: Optional[ResolvableInt] = None


ResolvableTransition = ResolvableModel(Transition)


# Pre-resolved list type to avoid class body name shadowing in Rule.
# The Rule class has a field named "NoncurrentVersionTransition" (default None) which shadows
# the NoncurrentVersionTransition class when Python evaluates List[NoncurrentVersionTransition] inside the class body.
_NoncurrentVersionTransitionList = Resolvable[List[NoncurrentVersionTransition]]


# Pre-resolved list type to avoid class body name shadowing in Rule.
# The Rule class has a field named "Transition" (default None) which shadows
# the Transition class when Python evaluates List[Transition] inside the class body.
_TransitionList = Resolvable[List[Transition]]


class Rule(CustomModel):
    """
    Specifies lifecycle rules for an Amazon S3 bucket.
    """

    Status: ResolvableStr
    AbortIncompleteMultipartUpload: Optional[ResolvableAbortIncompleteMultipartUpload] = None
    ExpirationDate: Optional[ResolvableStr] = None
    ExpirationInDays: Optional[ResolvableInt] = None
    ExpiredObjectDeleteMarker: Optional[ResolvableBool] = None
    Id: Optional[ResolvableStr] = None
    NoncurrentVersionExpiration: Optional[ResolvableNoncurrentVersionExpiration] = None
    NoncurrentVersionExpirationInDays: Optional[ResolvableInt] = None
    NoncurrentVersionTransition: Optional[ResolvableNoncurrentVersionTransition] = None
    NoncurrentVersionTransitions: Optional[_NoncurrentVersionTransitionList] = None
    ObjectSizeGreaterThan: Optional[ResolvableStr] = None
    ObjectSizeLessThan: Optional[ResolvableStr] = None
    Prefix: Optional[ResolvableStr] = None
    TagFilters: Optional[Resolvable[List[TagFilter]]] = None
    Transition: Optional[ResolvableTransition] = None
    Transitions: Optional[_TransitionList] = None


ResolvableRule = ResolvableModel(Rule)


class LifecycleConfiguration(CustomModel):
    """
    Specifies the lifecycle configuration for objects in an Amazon S3 bucket.
    """

    Rules: Resolvable[List[Rule]]
    TransitionDefaultMinimumObjectSize: Optional[ResolvableStr] = None


ResolvableLifecycleConfiguration = ResolvableModel(LifecycleConfiguration)


class S3BucketProperties(CustomModel):
    """
      Properties for AWS::S3::Bucket.

      Properties:

      - AbacStatus: The ABAC status of the general purpose bucket. When ABAC is enabled for the gene...
      - AccelerateConfiguration: Configures the transfer acceleration state for an Amazon S3 bucket. For more inf...
      - AccessControl: This is a legacy property, and it is not recommended for most use cases. A major...
      - AnalyticsConfigurations: Specifies the configuration and any analyses for the analytics filter of an Amaz...
      - BucketEncryption: Specifies default encryption for a bucket using server-side encryption with Amaz...
      - BucketName: A name for the bucket. If you don't specify a name, AWS CloudFormation generates...
      - CorsConfiguration: Describes the cross-origin access configuration for objects in an Amazon S3 buck...
      - IntelligentTieringConfigurations: Defines how Amazon S3 handles Intelligent-Tiering storage.
      - InventoryConfigurations: Specifies the S3 Inventory configuration for an Amazon S3 bucket. For more infor...
      - LifecycleConfiguration: Specifies the lifecycle configuration for objects in an Amazon S3 bucket. For mo...
      - LoggingConfiguration: Settings that define where logs are stored.
      - MetadataConfiguration: The S3 Metadata configuration for a general purpose bucket.
      - MetadataTableConfiguration: The metadata table configuration of an S3 general purpose bucket.
      - MetricsConfigurations: Specifies a metrics configuration for the CloudWatch request metrics (specified ...
      - NotificationConfiguration: Configuration that defines how Amazon S3 handles bucket notifications.
      - ObjectLockConfiguration: This operation is not supported for directory buckets.
    Places an Object Lock c...
      - ObjectLockEnabled: Indicates whether this bucket has an Object Lock configuration enabled. Enable `...
      - OwnershipControls: Configuration that defines how Amazon S3 handles Object Ownership rules.
      - PublicAccessBlockConfiguration: Configuration that defines how Amazon S3 handles public access.
      - ReplicationConfiguration: Configuration for replicating objects in an S3 bucket. To enable replication, yo...
      - Tags: An arbitrary set of tags (key-value pairs) for this S3 bucket.
      - VersioningConfiguration: Enables multiple versions of all objects in this bucket. You might enable versio...
      - WebsiteConfiguration: Information used to configure the bucket as a static website. For more informati...

      More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html)
    """

    AbacStatus: Optional[ResolvableStr] = None
    AccelerateConfiguration: Optional[ResolvableAccelerateConfiguration] = None
    AccessControl: Optional[ResolvableStr] = None
    AnalyticsConfigurations: Optional[Resolvable[List[AnalyticsConfiguration]]] = None
    BucketEncryption: Optional[ResolvableBucketEncryption] = None
    BucketName: Optional[ResolvableStr] = None
    CorsConfiguration: Optional[ResolvableCorsConfiguration] = None
    IntelligentTieringConfigurations: Optional[Resolvable[List[IntelligentTieringConfiguration]]] = None
    InventoryConfigurations: Optional[Resolvable[List[InventoryConfiguration]]] = None
    LifecycleConfiguration: Optional[ResolvableLifecycleConfiguration] = None
    LoggingConfiguration: Optional[ResolvableLoggingConfiguration] = None
    MetadataConfiguration: Optional[ResolvableMetadataConfiguration] = None
    MetadataTableConfiguration: Optional[ResolvableMetadataTableConfiguration] = None
    MetricsConfigurations: Optional[Resolvable[List[MetricsConfiguration]]] = None
    NotificationConfiguration: Optional[ResolvableNotificationConfiguration] = None
    ObjectLockConfiguration: Optional[ResolvableObjectLockConfiguration] = None
    ObjectLockEnabled: Optional[ResolvableBool] = None
    OwnershipControls: Optional[ResolvableOwnershipControls] = None
    PublicAccessBlockConfiguration: Optional[ResolvablePublicAccessBlockConfiguration] = None
    ReplicationConfiguration: Optional[ResolvableReplicationConfiguration] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VersioningConfiguration: Optional[ResolvableVersioningConfiguration] = None
    WebsiteConfiguration: Optional[ResolvableWebsiteConfiguration] = None


class S3Bucket(Resource):
    """
    The ``AWS::S3::Bucket`` resource creates an Amazon S3 bucket in the same AWS Region where you create the AWS CloudFormation stack.

    Properties:

    - Properties: A [S3BucketProperties][pycfmodel.model.resources.s3_bucket.S3BucketProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html)
    """

    Type: Literal["AWS::S3::Bucket"]
    Properties: Resolvable[S3BucketProperties] = S3BucketProperties()
