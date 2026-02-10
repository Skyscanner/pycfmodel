"""
DynamoDBTable resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::DynamoDB::Table.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableModel, ResolvableStr


class AttributeDefinition(CustomModel):
    """
    Represents an attribute for describing the schema for the table and indexes.
    """

    AttributeName: ResolvableStr
    AttributeType: ResolvableStr


ResolvableAttributeDefinition = ResolvableModel(AttributeDefinition)


class ContributorInsightsSpecification(CustomModel):
    """
    Configures contributor insights settings for a table or one of its indexes.
    """

    Enabled: ResolvableBool
    Mode: Optional[ResolvableStr] = None


ResolvableContributorInsightsSpecification = ResolvableModel(ContributorInsightsSpecification)


class Csv(CustomModel):
    """
    The options for imported source files in CSV format.
    """

    Delimiter: Optional[ResolvableStr] = None
    HeaderList: Optional[Resolvable[List[ResolvableStr]]] = None


ResolvableCsv = ResolvableModel(Csv)


class InputFormatOptions(CustomModel):
    """
    The format options for the data that was imported into the target table.
    """

    Csv: Optional[ResolvableCsv] = None


ResolvableInputFormatOptions = ResolvableModel(InputFormatOptions)


class KeySchema(CustomModel):
    """
    Represents *a single element* of a key schema.
    """

    AttributeName: ResolvableStr
    KeyType: ResolvableStr


ResolvableKeySchema = ResolvableModel(KeySchema)


class KinesisStreamSpecification(CustomModel):
    """
    The Kinesis Data Streams configuration for the specified table.
    """

    StreamArn: ResolvableStr
    ApproximateCreationDateTimePrecision: Optional[ResolvableStr] = None


ResolvableKinesisStreamSpecification = ResolvableModel(KinesisStreamSpecification)


class OnDemandThroughput(CustomModel):
    """
    Sets the maximum number of read and write units for the specified on-demand table.
    """

    MaxReadRequestUnits: Optional[ResolvableInt] = None
    MaxWriteRequestUnits: Optional[ResolvableInt] = None


ResolvableOnDemandThroughput = ResolvableModel(OnDemandThroughput)


class PointInTimeRecoverySpecification(CustomModel):
    """
    The settings used to enable point in time recovery.
    """

    PointInTimeRecoveryEnabled: Optional[ResolvableBool] = None
    RecoveryPeriodInDays: Optional[ResolvableInt] = None


ResolvablePointInTimeRecoverySpecification = ResolvableModel(PointInTimeRecoverySpecification)


class Projection(CustomModel):
    """
    Represents attributes that are copied (projected) from the table into an index.
    """

    NonKeyAttributes: Optional[Resolvable[List[ResolvableStr]]] = None
    ProjectionType: Optional[ResolvableStr] = None


ResolvableProjection = ResolvableModel(Projection)


# Pre-resolved list type to avoid class body name shadowing in LocalSecondaryIndex.
# The LocalSecondaryIndex class has a field named "KeySchema" (default None) which shadows
# the KeySchema class when Python evaluates List[KeySchema] inside the class body.
_KeySchemaList = Resolvable[List[KeySchema]]


class LocalSecondaryIndex(CustomModel):
    """
    Represents the properties of a local secondary index.
    """

    IndexName: ResolvableStr
    KeySchema: _KeySchemaList
    Projection: ResolvableProjection


ResolvableLocalSecondaryIndex = ResolvableModel(LocalSecondaryIndex)


class ProvisionedThroughput(CustomModel):
    """
    Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits``.
    """

    ReadCapacityUnits: ResolvableInt
    WriteCapacityUnits: ResolvableInt


ResolvableProvisionedThroughput = ResolvableModel(ProvisionedThroughput)


class ResourcePolicy(CustomModel):
    """
    Creates or updates a resource-based policy document that contains the permissions for DDB resources, such as a table, its indexes, and stream.
    """

    PolicyDocument: Resolvable[dict]


ResolvableResourcePolicy = ResolvableModel(ResourcePolicy)


class S3BucketSource(CustomModel):
    """
    The S3 bucket that is being imported from.
    """

    S3Bucket: ResolvableStr
    S3BucketOwner: Optional[ResolvableStr] = None
    S3KeyPrefix: Optional[ResolvableStr] = None


ResolvableS3BucketSource = ResolvableModel(S3BucketSource)


class ImportSourceSpecification(CustomModel):
    """
    Specifies the properties of data being imported from the S3 bucket source to the table.
    """

    InputFormat: ResolvableStr
    S3BucketSource: ResolvableS3BucketSource
    InputCompressionType: Optional[ResolvableStr] = None
    InputFormatOptions: Optional[ResolvableInputFormatOptions] = None


ResolvableImportSourceSpecification = ResolvableModel(ImportSourceSpecification)


class SSESpecification(CustomModel):
    """
    Represents the settings used to enable server-side encryption.
    """

    SSEEnabled: ResolvableBool
    KMSMasterKeyId: Optional[ResolvableStr] = None
    SSEType: Optional[ResolvableStr] = None


ResolvableSSESpecification = ResolvableModel(SSESpecification)


class StreamSpecification(CustomModel):
    """
    Represents the DynamoDB Streams configuration for a table in DynamoDB.
    """

    StreamViewType: ResolvableStr
    ResourcePolicy: Optional[ResolvableResourcePolicy] = None


ResolvableStreamSpecification = ResolvableModel(StreamSpecification)


class TimeToLiveSpecification(CustomModel):
    """
    Represents the settings used to enable or disable Time to Live (TTL) for the specified table.
    """

    Enabled: ResolvableBool
    AttributeName: Optional[ResolvableStr] = None


ResolvableTimeToLiveSpecification = ResolvableModel(TimeToLiveSpecification)


class WarmThroughput(CustomModel):
    """
    Provides visibility into the number of read and write operations your table or secondary index can instantaneously support.
    """

    ReadUnitsPerSecond: Optional[ResolvableInt] = None
    WriteUnitsPerSecond: Optional[ResolvableInt] = None


ResolvableWarmThroughput = ResolvableModel(WarmThroughput)


# Pre-resolved list type to avoid class body name shadowing in GlobalSecondaryIndex.
# The GlobalSecondaryIndex class has a field named "KeySchema" (default None) which shadows
# the KeySchema class when Python evaluates List[KeySchema] inside the class body.
_KeySchemaList = Resolvable[List[KeySchema]]


class GlobalSecondaryIndex(CustomModel):
    """
    Represents the properties of a global secondary index.
    """

    IndexName: ResolvableStr
    KeySchema: _KeySchemaList
    Projection: ResolvableProjection
    ContributorInsightsSpecification: Optional[ResolvableContributorInsightsSpecification] = None
    OnDemandThroughput: Optional[ResolvableOnDemandThroughput] = None
    ProvisionedThroughput: Optional[ResolvableProvisionedThroughput] = None
    WarmThroughput: Optional[ResolvableWarmThroughput] = None


ResolvableGlobalSecondaryIndex = ResolvableModel(GlobalSecondaryIndex)


# Pre-resolved list type to avoid class body name shadowing in DynamoDBTableProperties.
# The DynamoDBTableProperties class has a field named "KeySchema" (default None) which shadows
# the KeySchema class when Python evaluates List[KeySchema] inside the class body.
_KeySchemaList = Resolvable[List[KeySchema]]


class DynamoDBTableProperties(CustomModel):
    """
       Properties for AWS::DynamoDB::Table.

       Properties:

       - AttributeDefinitions: A list of attributes that describe the key schema for the table and indexes.
    Th...
       - BillingMode: Specify how you are charged for read and write throughput and how you manage cap...
       - ContributorInsightsSpecification: The settings used to specify whether to enable CloudWatch Contributor Insights f...
       - DeletionProtectionEnabled: Determines if a table is protected from deletion. When enabled, the table cannot...
       - GlobalSecondaryIndexes: Global secondary indexes to be created on the table. You can create up to 20 glo...
       - ImportSourceSpecification: Specifies the properties of data being imported from the S3 bucket source to the...
       - KeySchema: Specifies the attributes that make up the primary key for the table. The attribu...
       - KinesisStreamSpecification: The Kinesis Data Streams configuration for the specified table.
       - LocalSecondaryIndexes: Local secondary indexes to be created on the table. You can create up to 5 local...
       - OnDemandThroughput: Sets the maximum number of read and write units for the specified on-demand tabl...
       - PointInTimeRecoverySpecification: The settings used to enable point in time recovery.
       - ProvisionedThroughput: Throughput for the specified table, which consists of values for ``ReadCapacityU...
       - ResourcePolicy: An AWS resource-based policy document in JSON format that will be attached to th...
       - SSESpecification: Specifies the settings to enable server-side encryption.
       - StreamSpecification: The settings for the DDB table stream, which captures changes to items stored in...
       - TableClass: The table class of the new table. Valid values are ``STANDARD`` and ``STANDARD_I...
       - TableName: A name for the table. If you don't specify a name, CFNlong generates a unique ph...
       - Tags: An array of key-value pairs to apply to this resource.
    For more information, se...
       - TimeToLiveSpecification: Specifies the Time to Live (TTL) settings for the table.
     For detailed informat...
       - WarmThroughput: Represents the warm throughput (in read units per second and write units per sec...

       More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html)
    """

    KeySchema: _KeySchemaList
    AttributeDefinitions: Optional[Resolvable[List[AttributeDefinition]]] = None
    BillingMode: Optional[ResolvableStr] = None
    ContributorInsightsSpecification: Optional[ResolvableContributorInsightsSpecification] = None
    DeletionProtectionEnabled: Optional[ResolvableBool] = None
    GlobalSecondaryIndexes: Optional[Resolvable[List[GlobalSecondaryIndex]]] = None
    ImportSourceSpecification: Optional[ResolvableImportSourceSpecification] = None
    KinesisStreamSpecification: Optional[ResolvableKinesisStreamSpecification] = None
    LocalSecondaryIndexes: Optional[Resolvable[List[LocalSecondaryIndex]]] = None
    OnDemandThroughput: Optional[ResolvableOnDemandThroughput] = None
    PointInTimeRecoverySpecification: Optional[ResolvablePointInTimeRecoverySpecification] = None
    ProvisionedThroughput: Optional[ResolvableProvisionedThroughput] = None
    ResourcePolicy: Optional[ResolvableResourcePolicy] = None
    SSESpecification: Optional[ResolvableSSESpecification] = None
    StreamSpecification: Optional[ResolvableStreamSpecification] = None
    TableClass: Optional[ResolvableStr] = None
    TableName: Optional[ResolvableStr] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    TimeToLiveSpecification: Optional[ResolvableTimeToLiveSpecification] = None
    WarmThroughput: Optional[ResolvableWarmThroughput] = None


class DynamoDBTable(Resource):
    """
    The ``AWS::DynamoDB::Table`` resource creates a DDB table. For more information, see [CreateTable](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_CreateTable.html) in the *API Refe

    Properties:

    - Properties: A [DynamoDBTableProperties][pycfmodel.model.resources.dynamodb_table.DynamoDBTableProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html)
    """

    Type: Literal["AWS::DynamoDB::Table"]
    Properties: Resolvable[DynamoDBTableProperties]
