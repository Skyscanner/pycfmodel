"""
DynamoDBTable resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::DynamoDB::Table.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableStr


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

    KeySchema: Resolvable[List[ResolvableGeneric]]
    AttributeDefinitions: Optional[Resolvable[List[ResolvableGeneric]]] = None
    BillingMode: Optional[ResolvableStr] = None
    ContributorInsightsSpecification: Optional[ResolvableGeneric] = None
    DeletionProtectionEnabled: Optional[ResolvableBool] = None
    GlobalSecondaryIndexes: Optional[Resolvable[List[ResolvableGeneric]]] = None
    ImportSourceSpecification: Optional[ResolvableGeneric] = None
    KinesisStreamSpecification: Optional[ResolvableGeneric] = None
    LocalSecondaryIndexes: Optional[Resolvable[List[ResolvableGeneric]]] = None
    OnDemandThroughput: Optional[ResolvableGeneric] = None
    PointInTimeRecoverySpecification: Optional[ResolvableGeneric] = None
    ProvisionedThroughput: Optional[ResolvableGeneric] = None
    ResourcePolicy: Optional[ResolvableGeneric] = None
    SSESpecification: Optional[ResolvableGeneric] = None
    StreamSpecification: Optional[ResolvableGeneric] = None
    TableClass: Optional[ResolvableStr] = None
    TableName: Optional[ResolvableStr] = None
    Tags: Optional[Resolvable[List[ResolvableGeneric]]] = None
    TimeToLiveSpecification: Optional[ResolvableGeneric] = None
    WarmThroughput: Optional[ResolvableGeneric] = None


class DynamoDBTable(Resource):
    """
    The ``AWS::DynamoDB::Table`` resource creates a DDB table. For more information, see [CreateTable](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_CreateTable.html) in the *API Reference*.
 You should be aware of the following behaviors when working with DDB tables:
  +  CFNlong typically creates DDB tables in parallel. However, if your template includes multiple DDB tables with indexes, you must declare dependencies so that the tables are created sequentially. DDBlong limits the number of tables with secondary indexes that are in the creating state. If you create multiple tables with indexes at the same time, DDB returns an error and the stack operation fails. For an example, see [DynamoDB Table with a DependsOn Attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#aws-resource-dynamodb-table--examples--DynamoDB_Table_with_a_DependsOn_Attribute).
  
   Our guidance is to use the latest schema documented for your CFNlong templates. This schema supports the provisioning of all table settings below. When using this schema in your CFNlong templates, please ensure that your Identity and Access Management (IAM) policies are updated with appropriate permissions to allow for the authorization of these setting changes.

    Properties:

    - Properties: A [DynamoDBTableProperties][pycfmodel.model.resources.dynamodb_table.DynamoDBTableProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html)
    """

    Type: Literal["AWS::DynamoDB::Table"]
    Properties: Resolvable[DynamoDBTableProperties]
