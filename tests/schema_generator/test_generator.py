import pytest
from pydantic import ValidationError

from pycfmodel.model.base import FunctionDict
from pycfmodel.model.resources.resource import Resource
from pycfmodel.schema_generator import generate_resource_from_schema, get_schema_for_resource


class TestCloudFormationIntrinsicFunctions:
    """Test that dynamically generated resources properly handle CloudFormation intrinsic functions."""

    def test_ref_function(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {"Ref": "BucketNameParameter"},
            },
        )

        assert bucket.Properties.BucketName == FunctionDict(Ref="BucketNameParameter")

    def test_fn_sub_simple(self):
        DynamicLambdaFunction = generate_resource_from_schema("AWS::Lambda::Function")

        function = DynamicLambdaFunction(
            Type="AWS::Lambda::Function",
            Properties={
                "FunctionName": {"Fn::Sub": "${AWS::StackName}-my-function"},
                "Runtime": "python3.12",
                "Role": {"Fn::GetAtt": ["LambdaRole", "Arn"]},
                "Code": {"ZipFile": "def handler(event, context): pass"},
            },
        )

        assert function.Properties.FunctionName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-my-function"})

    def test_fn_sub_with_mapping(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {"Fn::Sub": ["${Prefix}-bucket", {"Prefix": "my-app"}]},
            },
        )

        assert bucket.Properties.BucketName == FunctionDict(**{"Fn::Sub": ["${Prefix}-bucket", {"Prefix": "my-app"}]})

    def test_fn_get_att(self):
        DynamicLambdaFunction = generate_resource_from_schema("AWS::Lambda::Function")

        function = DynamicLambdaFunction(
            Type="AWS::Lambda::Function",
            Properties={
                "FunctionName": "my-function",
                "Runtime": "python3.12",
                "Role": {"Fn::GetAtt": ["LambdaExecutionRole", "Arn"]},
                "Code": {"ZipFile": "def handler(event, context): pass"},
            },
        )

        assert function.Properties.Role == FunctionDict(**{"Fn::GetAtt": ["LambdaExecutionRole", "Arn"]})

    def test_fn_join(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {"Fn::Join": ["-", ["my", "bucket", "name"]]},
            },
        )

        assert bucket.Properties.BucketName == FunctionDict(**{"Fn::Join": ["-", ["my", "bucket", "name"]]})

    def test_fn_select(self):
        DynamicEC2Instance = generate_resource_from_schema("AWS::EC2::Instance")

        instance = DynamicEC2Instance(
            Type="AWS::EC2::Instance",
            Properties={
                "ImageId": "ami-12345678",
                "InstanceType": "t2.micro",
                "SubnetId": {"Fn::Select": ["0", {"Ref": "SubnetIds"}]},
            },
        )

        assert instance.Properties.SubnetId == FunctionDict(**{"Fn::Select": ["0", {"Ref": "SubnetIds"}]})

    def test_fn_split(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {"Fn::Select": ["0", {"Fn::Split": ["-", "my-bucket-name"]}]},
            },
        )

        expected = FunctionDict(**{"Fn::Select": ["0", {"Fn::Split": ["-", "my-bucket-name"]}]})
        assert bucket.Properties.BucketName == expected

    def test_fn_if(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {"Fn::If": ["CreateProdResources", "prod-bucket", "dev-bucket"]},
            },
        )

        assert bucket.Properties.BucketName == FunctionDict(
            **{"Fn::If": ["CreateProdResources", "prod-bucket", "dev-bucket"]}
        )

    def test_fn_import_value(self):
        DynamicLambdaFunction = generate_resource_from_schema("AWS::Lambda::Function")

        function = DynamicLambdaFunction(
            Type="AWS::Lambda::Function",
            Properties={
                "FunctionName": "my-function",
                "Runtime": "python3.12",
                "Role": {"Fn::ImportValue": "SharedLambdaRoleArn"},
                "Code": {"ZipFile": "def handler(event, context): pass"},
            },
        )

        assert function.Properties.Role == FunctionDict(**{"Fn::ImportValue": "SharedLambdaRoleArn"})

    def test_fn_find_in_map(self):
        DynamicEC2Instance = generate_resource_from_schema("AWS::EC2::Instance")

        instance = DynamicEC2Instance(
            Type="AWS::EC2::Instance",
            Properties={
                "ImageId": {"Fn::FindInMap": ["RegionMap", {"Ref": "AWS::Region"}, "AMI"]},
                "InstanceType": "t2.micro",
            },
        )

        assert instance.Properties.ImageId == FunctionDict(
            **{"Fn::FindInMap": ["RegionMap", {"Ref": "AWS::Region"}, "AMI"]}
        )

    def test_fn_base64(self):
        DynamicEC2Instance = generate_resource_from_schema("AWS::EC2::Instance")

        instance = DynamicEC2Instance(
            Type="AWS::EC2::Instance",
            Properties={
                "ImageId": "ami-12345678",
                "InstanceType": "t2.micro",
                "UserData": {"Fn::Base64": "#!/bin/bash\necho Hello World"},
            },
        )

        assert instance.Properties.UserData == FunctionDict(**{"Fn::Base64": "#!/bin/bash\necho Hello World"})

    def test_fn_get_azs(self):
        DynamicEC2Subnet = generate_resource_from_schema("AWS::EC2::Subnet")

        subnet = DynamicEC2Subnet(
            Type="AWS::EC2::Subnet",
            Properties={
                "VpcId": {"Ref": "MyVPC"},
                "CidrBlock": "10.0.0.0/24",
                "AvailabilityZone": {"Fn::Select": ["0", {"Fn::GetAZs": {"Ref": "AWS::Region"}}]},
            },
        )

        expected_az = FunctionDict(**{"Fn::Select": ["0", {"Fn::GetAZs": {"Ref": "AWS::Region"}}]})
        assert subnet.Properties.AvailabilityZone == expected_az

    def test_nested_intrinsic_functions(self):
        DynamicLambdaFunction = generate_resource_from_schema("AWS::Lambda::Function")

        function = DynamicLambdaFunction(
            Type="AWS::Lambda::Function",
            Properties={
                "FunctionName": {
                    "Fn::Join": [
                        "-",
                        [
                            {"Ref": "AWS::StackName"},
                            {"Fn::If": ["IsProd", "prod", "dev"]},
                            "function",
                        ],
                    ]
                },
                "Runtime": "python3.12",
                "Role": {"Fn::GetAtt": ["LambdaRole", "Arn"]},
                "Code": {"ZipFile": "def handler(event, context): pass"},
            },
        )

        expected_name = FunctionDict(
            **{
                "Fn::Join": [
                    "-",
                    [
                        {"Ref": "AWS::StackName"},
                        {"Fn::If": ["IsProd", "prod", "dev"]},
                        "function",
                    ],
                ]
            }
        )
        assert function.Properties.FunctionName == expected_name


class TestCloudFormationConditions:
    """Test that dynamically generated resources properly handle CloudFormation conditions."""

    def test_resource_with_condition(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Condition="CreateBucketCondition",
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.Condition == "CreateBucketCondition"

    def test_property_with_fn_if_condition(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {"Fn::If": ["IsProd", "prod-bucket", {"Ref": "AWS::NoValue"}]},
                "AccessControl": {"Fn::If": ["IsPrivate", "Private", "PublicRead"]},
            },
        )

        assert bucket.Properties.BucketName == FunctionDict(
            **{"Fn::If": ["IsProd", "prod-bucket", {"Ref": "AWS::NoValue"}]}
        )
        assert bucket.Properties.AccessControl == FunctionDict(**{"Fn::If": ["IsPrivate", "Private", "PublicRead"]})

    def test_fn_and_condition(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {
                    "Fn::If": [
                        {"Fn::And": [{"Condition": "IsProd"}, {"Condition": "IsEnabled"}]},
                        "enabled-prod-bucket",
                        "other-bucket",
                    ]
                },
            },
        )

        expected = FunctionDict(
            **{
                "Fn::If": [
                    {"Fn::And": [{"Condition": "IsProd"}, {"Condition": "IsEnabled"}]},
                    "enabled-prod-bucket",
                    "other-bucket",
                ]
            }
        )
        assert bucket.Properties.BucketName == expected

    def test_fn_or_condition(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {
                    "Fn::If": [
                        {"Fn::Or": [{"Condition": "IsProd"}, {"Condition": "IsStaging"}]},
                        "important-bucket",
                        "dev-bucket",
                    ]
                },
            },
        )

        expected = FunctionDict(
            **{
                "Fn::If": [
                    {"Fn::Or": [{"Condition": "IsProd"}, {"Condition": "IsStaging"}]},
                    "important-bucket",
                    "dev-bucket",
                ]
            }
        )
        assert bucket.Properties.BucketName == expected

    def test_fn_not_condition(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {
                    "Fn::If": [
                        {"Fn::Not": [{"Condition": "IsDev"}]},
                        "non-dev-bucket",
                        "dev-bucket",
                    ]
                },
            },
        )

        expected = FunctionDict(
            **{
                "Fn::If": [
                    {"Fn::Not": [{"Condition": "IsDev"}]},
                    "non-dev-bucket",
                    "dev-bucket",
                ]
            }
        )
        assert bucket.Properties.BucketName == expected

    def test_fn_equals_condition(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {
                    "Fn::If": [
                        {"Fn::Equals": [{"Ref": "Environment"}, "prod"]},
                        "production-bucket",
                        "non-prod-bucket",
                    ]
                },
            },
        )

        expected = FunctionDict(
            **{
                "Fn::If": [
                    {"Fn::Equals": [{"Ref": "Environment"}, "prod"]},
                    "production-bucket",
                    "non-prod-bucket",
                ]
            }
        )
        assert bucket.Properties.BucketName == expected


class TestResourceMetadataAttributes:
    """Test that dynamically generated resources properly handle CloudFormation resource attributes."""

    def test_depends_on_single(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            DependsOn="MyVPC",
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.DependsOn == "MyVPC"

    def test_depends_on_multiple(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            DependsOn=["MyVPC", "MySecurityGroup"],
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.DependsOn == ["MyVPC", "MySecurityGroup"]

    def test_deletion_policy(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            DeletionPolicy="Retain",
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.DeletionPolicy == "Retain"

    def test_update_replace_policy(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            UpdateReplacePolicy="Snapshot",
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.UpdateReplacePolicy == "Snapshot"

    def test_metadata(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Metadata={
                "AWS::CloudFormation::Designer": {"id": "12345"},
                "Comment": "This is a test bucket",
            },
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.Metadata == {
            "AWS::CloudFormation::Designer": {"id": "12345"},
            "Comment": "This is a test bucket",
        }

    def test_all_resource_attributes_together(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Condition="CreateBucket",
            DependsOn=["VPC", "SecurityGroup"],
            DeletionPolicy="Retain",
            UpdateReplacePolicy="Retain",
            Metadata={"Comment": "Important bucket"},
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.Condition == "CreateBucket"
        assert bucket.DependsOn == ["VPC", "SecurityGroup"]
        assert bucket.DeletionPolicy == "Retain"
        assert bucket.UpdateReplacePolicy == "Retain"
        assert bucket.Metadata == {"Comment": "Important bucket"}


class TestGetSchemaForResource:
    def test_get_schema_for_existing_resource(self):
        schema = get_schema_for_resource("AWS::S3::Bucket")
        assert schema is not None
        assert schema["typeName"] == "AWS::S3::Bucket"
        assert "properties" in schema
        assert "definitions" in schema

    def test_get_schema_for_nonexistent_resource(self):
        schema = get_schema_for_resource("AWS::Fake::Resource")
        assert schema is None

    def test_get_schema_for_lambda_function(self):
        schema = get_schema_for_resource("AWS::Lambda::Function")
        assert schema is not None
        assert schema["typeName"] == "AWS::Lambda::Function"
        assert "FunctionName" in schema["properties"]
        assert "Runtime" in schema["properties"]


class TestGenerateResourceFromSchema:
    def test_generate_s3_bucket(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        assert issubclass(DynamicS3Bucket, Resource)
        assert DynamicS3Bucket.__name__ == "S3Bucket"

        # Create an instance
        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": "my-test-bucket",
                "Tags": [{"Key": "Environment", "Value": "test"}],
            },
        )

        assert bucket.Type == "AWS::S3::Bucket"
        assert bucket.Properties.BucketName == "my-test-bucket"

    def test_generate_lambda_function(self):
        DynamicLambdaFunction = generate_resource_from_schema("AWS::Lambda::Function")

        assert issubclass(DynamicLambdaFunction, Resource)
        assert DynamicLambdaFunction.__name__ == "LambdaFunction"

        # Create an instance with minimal properties
        function = DynamicLambdaFunction(
            Type="AWS::Lambda::Function",
            Properties={
                "FunctionName": "my-function",
                "Runtime": "python3.12",
                "Role": "arn:aws:iam::123456789012:role/lambda-role",
                "Code": {"ZipFile": "def handler(event, context): return 'Hello'"},
            },
        )

        assert function.Type == "AWS::Lambda::Function"
        assert function.Properties.FunctionName == "my-function"
        assert function.Properties.Runtime == "python3.12"

    def test_generate_dynamodb_table(self):
        DynamicDynamoDBTable = generate_resource_from_schema("AWS::DynamoDB::Table")

        assert issubclass(DynamicDynamoDBTable, Resource)
        assert DynamicDynamoDBTable.__name__ == "DynamoDBTable"

        # Create an instance
        table = DynamicDynamoDBTable(
            Type="AWS::DynamoDB::Table",
            Properties={
                "TableName": "my-table",
                "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
                "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
                "BillingMode": "PAY_PER_REQUEST",
            },
        )

        assert table.Type == "AWS::DynamoDB::Table"
        assert table.Properties.TableName == "my-table"

    def test_generate_nonexistent_resource_raises_error(self):
        with pytest.raises(ValueError, match="not found in CloudFormation schema registry"):
            generate_resource_from_schema("AWS::Fake::Resource")

    def test_generated_resource_supports_cloudformation_functions(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        # Test with Ref function
        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={
                "BucketName": {"Ref": "BucketNameParameter"},
            },
        )

        assert bucket.Properties.BucketName == FunctionDict(Ref="BucketNameParameter")

    def test_generated_resource_supports_sub_function(self):
        DynamicLambdaFunction = generate_resource_from_schema("AWS::Lambda::Function")

        function = DynamicLambdaFunction(
            Type="AWS::Lambda::Function",
            Properties={
                "FunctionName": {"Fn::Sub": "${AWS::StackName}-function"},
                "Runtime": "python3.12",
                "Role": {"Fn::GetAtt": ["LambdaRole", "Arn"]},
                "Code": {"ZipFile": "def handler(event, context): pass"},
            },
        )

        assert function.Properties.FunctionName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-function"})
        assert function.Properties.Role == FunctionDict(**{"Fn::GetAtt": ["LambdaRole", "Arn"]})

    def test_generated_resource_with_optional_properties(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        # Create bucket with no properties
        bucket = DynamicS3Bucket(Type="AWS::S3::Bucket")
        assert bucket.Properties is None

        # Create bucket with empty properties
        bucket = DynamicS3Bucket(Type="AWS::S3::Bucket", Properties={})
        assert bucket.Properties is not None
        assert bucket.Properties.BucketName is None

    def test_generated_resource_wrong_type_raises_error(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        with pytest.raises(ValidationError):
            DynamicS3Bucket(
                Type="AWS::Lambda::Function",  # Wrong type
                Properties={"BucketName": "test"},
            )

    def test_generated_resource_has_schema_metadata(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        assert hasattr(DynamicS3Bucket, "_schema")
        assert DynamicS3Bucket._schema["typeName"] == "AWS::S3::Bucket"
        assert hasattr(DynamicS3Bucket, "_properties_model")

    def test_generate_sns_topic(self):
        DynamicSNSTopic = generate_resource_from_schema("AWS::SNS::Topic")

        assert issubclass(DynamicSNSTopic, Resource)
        assert DynamicSNSTopic.__name__ == "SNSTopic"

        topic = DynamicSNSTopic(
            Type="AWS::SNS::Topic",
            Properties={
                "TopicName": "my-topic",
                "DisplayName": "My Topic",
            },
        )

        assert topic.Type == "AWS::SNS::Topic"
        assert topic.Properties.TopicName == "my-topic"

    def test_generate_sqs_queue(self):
        DynamicSQSQueue = generate_resource_from_schema("AWS::SQS::Queue")

        assert issubclass(DynamicSQSQueue, Resource)

        queue = DynamicSQSQueue(
            Type="AWS::SQS::Queue",
            Properties={
                "QueueName": "my-queue",
                "VisibilityTimeout": 30,
            },
        )

        assert queue.Type == "AWS::SQS::Queue"
        assert queue.Properties.QueueName == "my-queue"
        assert queue.Properties.VisibilityTimeout == 30

    def test_generate_ec2_instance(self):
        DynamicEC2Instance = generate_resource_from_schema("AWS::EC2::Instance")

        assert issubclass(DynamicEC2Instance, Resource)

        instance = DynamicEC2Instance(
            Type="AWS::EC2::Instance",
            Properties={
                "ImageId": "ami-12345678",
                "InstanceType": "t2.micro",
            },
        )

        assert instance.Type == "AWS::EC2::Instance"
        assert instance.Properties.ImageId == "ami-12345678"
        assert instance.Properties.InstanceType == "t2.micro"


class TestGeneratedResourceIntegration:
    def test_resource_inherits_base_resource_fields(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            DependsOn=["OtherResource"],
            Condition="CreateBucketCondition",
            DeletionPolicy="Retain",
            Properties={"BucketName": "my-bucket"},
        )

        assert bucket.DependsOn == ["OtherResource"]
        assert bucket.Condition == "CreateBucketCondition"
        assert bucket.DeletionPolicy == "Retain"

    def test_resource_serialization(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={"BucketName": "my-bucket"},
        )

        # Test model_dump
        data = bucket.model_dump(exclude_none=True)
        assert data["Type"] == "AWS::S3::Bucket"
        assert data["Properties"]["BucketName"] == "my-bucket"

    def test_multiple_resources_same_type(self):
        DynamicS3Bucket = generate_resource_from_schema("AWS::S3::Bucket")

        bucket1 = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={"BucketName": "bucket-1"},
        )

        bucket2 = DynamicS3Bucket(
            Type="AWS::S3::Bucket",
            Properties={"BucketName": "bucket-2"},
        )

        assert bucket1.Properties.BucketName == "bucket-1"
        assert bucket2.Properties.BucketName == "bucket-2"
