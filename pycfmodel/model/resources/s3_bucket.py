from typing import ClassVar, List, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableDict, ResolvableStr


class S3BucketProperties(CustomModel):
    """
    Properties:

    - AccelerateConfiguration: Configures the transfer acceleration state for an Amazon S3 bucket.
    - AccessControl: A canned access control list (ACL) that grants predefined permissions to the bucket.
    - AnalyticsConfigurations: Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.
    - BucketEncryption: Specifies encryption on the bucket.
    - BucketName: The name of the bucket.
    - CorsConfiguration: Describes the cross-origin access configuration for objects in an Amazon S3 bucket.
    - IntelligentTieringConfigurations: Defines how Amazon S3 handles Intelligent-Tiering storage.
    - InventoryConfigurations: Specifies the inventory configuration for an Amazon S3 bucket.
    - LifecycleConfiguration: Specifies the lifecycle configuration for objects in an Amazon S3 bucket.
    - LoggingConfiguration: Settings that define where logs are stored.
    - MetricsConfigurations: Specifies a metrics configuration for the CloudWatch request metrics.
    - NotificationConfiguration: Defines how Amazon S3 handles bucket notifications.
    - ObjectLockConfiguration: Places an Object Lock configuration on the specified bucket.
    - ObjectLockEnabled: Indicates whether this bucket has an Object Lock configuration enabled.
    - OwnershipControls: Defines how Amazon S3 handles object ownership rules.
    - PublicAccessBlockConfiguration: Defines how Amazon S3 handles public access.
    - ReplicationConfiguration: Configuration for replicating objects in an S3 bucket.
    - Tags: An arbitrary set of tags (key-value pairs) for the bucket.
    - VersioningConfiguration: If enabled, allows for multiple versions of all objects in this bucket to be stored.
    - WebsiteConfiguration: Information used to configure the bucket as a static website.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)
    """

    AccelerateConfiguration: Optional[ResolvableDict] = None
    AccessControl: Optional[ResolvableStr] = None
    AnalyticsConfigurations: Optional[Resolvable[List[ResolvableDict]]] = None
    BucketEncryption: Optional[ResolvableDict] = None
    BucketName: Optional[ResolvableStr] = None
    CorsConfiguration: Optional[ResolvableDict] = None
    IntelligentTieringConfigurations: Optional[Resolvable[List[ResolvableDict]]] = None
    InventoryConfigurations: Optional[Resolvable[List[ResolvableDict]]] = None
    LifecycleConfiguration: Optional[ResolvableDict] = None
    LoggingConfiguration: Optional[ResolvableDict] = None
    MetricsConfigurations: Optional[Resolvable[List[ResolvableDict]]] = None
    NotificationConfiguration: Optional[ResolvableDict] = None
    ObjectLockConfiguration: Optional[ResolvableDict] = None
    ObjectLockEnabled: Optional[ResolvableBool] = None
    OwnershipControls: Optional[ResolvableDict] = None
    PublicAccessBlockConfiguration: Optional[ResolvableDict] = None
    ReplicationConfiguration: Optional[ResolvableDict] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VersioningConfiguration: Optional[ResolvableDict] = None
    WebsiteConfiguration: Optional[ResolvableDict] = None


class S3Bucket(Resource):
    """
    Properties:

    - Properties: A [S3 Bucket Properties][pycfmodel.model.resources.s3_bucket.S3BucketProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)
    """

    TYPE_VALUE: ClassVar = "AWS::S3::Bucket"
    Type: str = TYPE_VALUE
    Properties: Resolvable[S3BucketProperties]
