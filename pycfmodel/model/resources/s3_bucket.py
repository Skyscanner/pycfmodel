from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableStr


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

    AccelerateConfiguration: Optional[ResolvableGeneric] = None
    AccessControl: Optional[ResolvableStr] = None
    AnalyticsConfigurations: Optional[Resolvable[List[ResolvableGeneric]]] = None
    BucketEncryption: Optional[ResolvableGeneric] = None
    BucketName: Optional[ResolvableStr] = None
    CorsConfiguration: Optional[ResolvableGeneric] = None
    IntelligentTieringConfigurations: Optional[Resolvable[List[ResolvableGeneric]]] = None
    InventoryConfigurations: Optional[Resolvable[List[ResolvableGeneric]]] = None
    LifecycleConfiguration: Optional[ResolvableGeneric] = None
    LoggingConfiguration: Optional[ResolvableGeneric] = None
    MetricsConfigurations: Optional[Resolvable[List[ResolvableGeneric]]] = None
    NotificationConfiguration: Optional[ResolvableGeneric] = None
    ObjectLockConfiguration: Optional[ResolvableGeneric] = None
    ObjectLockEnabled: Optional[ResolvableBool] = None
    OwnershipControls: Optional[ResolvableGeneric] = None
    PublicAccessBlockConfiguration: Optional[ResolvableGeneric] = None
    ReplicationConfiguration: Optional[ResolvableGeneric] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VersioningConfiguration: Optional[ResolvableGeneric] = None
    WebsiteConfiguration: Optional[ResolvableGeneric] = None


class S3Bucket(Resource):
    """
    Properties:

    - Properties: A [S3 Bucket Properties][pycfmodel.model.resources.s3_bucket.S3BucketProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)
    """

    Type: Literal["AWS::S3::Bucket"]
    Properties: Resolvable[S3BucketProperties]
