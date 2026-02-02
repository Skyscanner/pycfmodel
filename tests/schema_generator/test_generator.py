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


class TestFullCloudFormationTemplate:
    """Test parsing a complete CloudFormation template with ECS cluster, ALB, and related resources."""

    @pytest.fixture
    def ecs_alb_template(self):
        """A realistic CloudFormation template for ECS with ALB."""
        return {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "ECS Cluster with ALB and Fargate Service",
            "Parameters": {
                "VpcId": {"Type": "AWS::EC2::VPC::Id", "Description": "VPC ID"},
                "SubnetIds": {
                    "Type": "List<AWS::EC2::Subnet::Id>",
                    "Description": "Subnet IDs for the ECS tasks and ALB",
                },
                "ContainerImage": {
                    "Type": "String",
                    "Default": "nginx:latest",
                    "Description": "Docker image for the container",
                },
                "ContainerPort": {"Type": "Number", "Default": 80, "Description": "Container port"},
                "DesiredCount": {"Type": "Number", "Default": 2, "Description": "Desired task count"},
                "Environment": {
                    "Type": "String",
                    "AllowedValues": ["dev", "staging", "prod"],
                    "Default": "dev",
                },
            },
            "Conditions": {
                "IsProd": {"Fn::Equals": [{"Ref": "Environment"}, "prod"]},
                "IsNotDev": {"Fn::Not": [{"Fn::Equals": [{"Ref": "Environment"}, "dev"]}]},
            },
            "Resources": {
                # ECS Cluster
                "ECSCluster": {
                    "Type": "AWS::ECS::Cluster",
                    "Properties": {
                        "ClusterName": {"Fn::Sub": "${AWS::StackName}-cluster"},
                        "ClusterSettings": [{"Name": "containerInsights", "Value": "enabled"}],
                        "Tags": [
                            {"Key": "Environment", "Value": {"Ref": "Environment"}},
                            {"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-cluster"}},
                        ],
                    },
                },
                # ALB Security Group
                "ALBSecurityGroup": {
                    "Type": "AWS::EC2::SecurityGroup",
                    "Properties": {
                        "GroupDescription": "Security group for ALB",
                        "VpcId": {"Ref": "VpcId"},
                        "SecurityGroupIngress": [
                            {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "CidrIp": "0.0.0.0/0"},
                            {"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443, "CidrIp": "0.0.0.0/0"},
                        ],
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-alb-sg"}}],
                    },
                },
                # ECS Tasks Security Group
                "ECSSecurityGroup": {
                    "Type": "AWS::EC2::SecurityGroup",
                    "Properties": {
                        "GroupDescription": "Security group for ECS tasks",
                        "VpcId": {"Ref": "VpcId"},
                        "SecurityGroupIngress": [
                            {
                                "IpProtocol": "tcp",
                                "FromPort": {"Ref": "ContainerPort"},
                                "ToPort": {"Ref": "ContainerPort"},
                                "SourceSecurityGroupId": {"Ref": "ALBSecurityGroup"},
                            }
                        ],
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-ecs-sg"}}],
                    },
                },
                # Application Load Balancer
                "ApplicationLoadBalancer": {
                    "Type": "AWS::ElasticLoadBalancingV2::LoadBalancer",
                    "Properties": {
                        "Name": {"Fn::Sub": "${AWS::StackName}-alb"},
                        "Scheme": "internet-facing",
                        "Type": "application",
                        "Subnets": {"Ref": "SubnetIds"},
                        "SecurityGroups": [{"Ref": "ALBSecurityGroup"}],
                        "Tags": [
                            {"Key": "Environment", "Value": {"Ref": "Environment"}},
                            {"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-alb"}},
                        ],
                    },
                },
                # Target Group
                "TargetGroup": {
                    "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
                    "Properties": {
                        "Name": {"Fn::Sub": "${AWS::StackName}-tg"},
                        "Port": {"Ref": "ContainerPort"},
                        "Protocol": "HTTP",
                        "VpcId": {"Ref": "VpcId"},
                        "TargetType": "ip",
                        "HealthCheckPath": "/health",
                        "HealthCheckProtocol": "HTTP",
                        "HealthCheckIntervalSeconds": 30,
                        "HealthCheckTimeoutSeconds": 5,
                        "HealthyThresholdCount": 2,
                        "UnhealthyThresholdCount": 3,
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-tg"}}],
                    },
                },
                # ALB Listener
                "ALBListener": {
                    "Type": "AWS::ElasticLoadBalancingV2::Listener",
                    "Properties": {
                        "LoadBalancerArn": {"Ref": "ApplicationLoadBalancer"},
                        "Port": 80,
                        "Protocol": "HTTP",
                        "DefaultActions": [{"Type": "forward", "TargetGroupArn": {"Ref": "TargetGroup"}}],
                    },
                },
                # IAM Role for ECS Task Execution
                "ECSTaskExecutionRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {
                        "RoleName": {"Fn::Sub": "${AWS::StackName}-ecs-execution-role"},
                        "AssumeRolePolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                                    "Action": "sts:AssumeRole",
                                }
                            ],
                        },
                        "ManagedPolicyArns": ["arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"],
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-ecs-execution-role"}}],
                    },
                },
                # IAM Role for ECS Task
                "ECSTaskRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {
                        "RoleName": {"Fn::Sub": "${AWS::StackName}-ecs-task-role"},
                        "AssumeRolePolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                                    "Action": "sts:AssumeRole",
                                }
                            ],
                        },
                        "Policies": [
                            {
                                "PolicyName": "ECSTaskPolicy",
                                "PolicyDocument": {
                                    "Version": "2012-10-17",
                                    "Statement": [
                                        {
                                            "Effect": "Allow",
                                            "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
                                            "Resource": "*",
                                        }
                                    ],
                                },
                            }
                        ],
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-ecs-task-role"}}],
                    },
                },
                # CloudWatch Log Group
                "LogGroup": {
                    "Type": "AWS::Logs::LogGroup",
                    "Properties": {
                        "LogGroupName": {"Fn::Sub": "/ecs/${AWS::StackName}"},
                        "RetentionInDays": {"Fn::If": ["IsProd", 90, 14]},
                    },
                },
                # ECS Task Definition
                "TaskDefinition": {
                    "Type": "AWS::ECS::TaskDefinition",
                    "Properties": {
                        "Family": {"Fn::Sub": "${AWS::StackName}-task"},
                        "NetworkMode": "awsvpc",
                        "RequiresCompatibilities": ["FARGATE"],
                        "Cpu": {"Fn::If": ["IsProd", "1024", "256"]},
                        "Memory": {"Fn::If": ["IsProd", "2048", "512"]},
                        "ExecutionRoleArn": {"Fn::GetAtt": ["ECSTaskExecutionRole", "Arn"]},
                        "TaskRoleArn": {"Fn::GetAtt": ["ECSTaskRole", "Arn"]},
                        "ContainerDefinitions": [
                            {
                                "Name": "app",
                                "Image": {"Ref": "ContainerImage"},
                                "Essential": True,
                                "PortMappings": [{"ContainerPort": {"Ref": "ContainerPort"}, "Protocol": "tcp"}],
                                "LogConfiguration": {
                                    "LogDriver": "awslogs",
                                    "Options": {
                                        "awslogs-group": {"Ref": "LogGroup"},
                                        "awslogs-region": {"Ref": "AWS::Region"},
                                        "awslogs-stream-prefix": "ecs",
                                    },
                                },
                                "Environment": [
                                    {"Name": "ENVIRONMENT", "Value": {"Ref": "Environment"}},
                                    {"Name": "PORT", "Value": {"Ref": "ContainerPort"}},
                                ],
                            }
                        ],
                        "Tags": [{"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-task"}}],
                    },
                },
                # ECS Service
                "ECSService": {
                    "Type": "AWS::ECS::Service",
                    "DependsOn": ["ALBListener"],
                    "Properties": {
                        "ServiceName": {"Fn::Sub": "${AWS::StackName}-service"},
                        "Cluster": {"Ref": "ECSCluster"},
                        "TaskDefinition": {"Ref": "TaskDefinition"},
                        "DesiredCount": {"Ref": "DesiredCount"},
                        "LaunchType": "FARGATE",
                        "NetworkConfiguration": {
                            "AwsvpcConfiguration": {
                                "Subnets": {"Ref": "SubnetIds"},
                                "SecurityGroups": [{"Ref": "ECSSecurityGroup"}],
                                "AssignPublicIp": "ENABLED",
                            }
                        },
                        "LoadBalancers": [
                            {
                                "ContainerName": "app",
                                "ContainerPort": {"Ref": "ContainerPort"},
                                "TargetGroupArn": {"Ref": "TargetGroup"},
                            }
                        ],
                        "DeploymentConfiguration": {
                            "MinimumHealthyPercent": 50,
                            "MaximumPercent": 200,
                        },
                        "Tags": [
                            {"Key": "Environment", "Value": {"Ref": "Environment"}},
                            {"Key": "Name", "Value": {"Fn::Sub": "${AWS::StackName}-service"}},
                        ],
                    },
                },
                # Auto Scaling Target (only in prod)
                "AutoScalingTarget": {
                    "Type": "AWS::ApplicationAutoScaling::ScalableTarget",
                    "Condition": "IsProd",
                    "Properties": {
                        "MaxCapacity": 10,
                        "MinCapacity": 2,
                        "ResourceId": {
                            "Fn::Join": [
                                "/",
                                [
                                    "service",
                                    {"Ref": "ECSCluster"},
                                    {"Fn::GetAtt": ["ECSService", "Name"]},
                                ],
                            ]
                        },
                        "ScalableDimension": "ecs:service:DesiredCount",
                        "ServiceNamespace": "ecs",
                    },
                },
                # Auto Scaling Policy (only in prod)
                "AutoScalingPolicy": {
                    "Type": "AWS::ApplicationAutoScaling::ScalingPolicy",
                    "Condition": "IsProd",
                    "Properties": {
                        "PolicyName": {"Fn::Sub": "${AWS::StackName}-scaling-policy"},
                        "PolicyType": "TargetTrackingScaling",
                        "ScalingTargetId": {"Ref": "AutoScalingTarget"},
                        "TargetTrackingScalingPolicyConfiguration": {
                            "PredefinedMetricSpecification": {
                                "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
                            },
                            "TargetValue": 70,
                            "ScaleInCooldown": 300,
                            "ScaleOutCooldown": 60,
                        },
                    },
                },
            },
            "Outputs": {
                "ClusterArn": {
                    "Description": "ECS Cluster ARN",
                    "Value": {"Fn::GetAtt": ["ECSCluster", "Arn"]},
                    "Export": {"Name": {"Fn::Sub": "${AWS::StackName}-cluster-arn"}},
                },
                "ServiceName": {
                    "Description": "ECS Service Name",
                    "Value": {"Fn::GetAtt": ["ECSService", "Name"]},
                },
                "LoadBalancerDNS": {
                    "Description": "ALB DNS Name",
                    "Value": {"Fn::GetAtt": ["ApplicationLoadBalancer", "DNSName"]},
                },
                "LoadBalancerURL": {
                    "Description": "URL of the load balancer",
                    "Value": {"Fn::Sub": "http://${ApplicationLoadBalancer.DNSName}"},
                },
            },
        }

    def test_parse_ecs_alb_template_with_dynamic_models(self, ecs_alb_template):
        """Test that all resources in a realistic ECS+ALB template can be parsed with dynamic models."""
        # Generate all required resource models
        resource_types = [
            "AWS::ECS::Cluster",
            "AWS::ECS::TaskDefinition",
            "AWS::ECS::Service",
            "AWS::EC2::SecurityGroup",
            "AWS::ElasticLoadBalancingV2::LoadBalancer",
            "AWS::ElasticLoadBalancingV2::TargetGroup",
            "AWS::ElasticLoadBalancingV2::Listener",
            "AWS::IAM::Role",
            "AWS::Logs::LogGroup",
            "AWS::ApplicationAutoScaling::ScalableTarget",
            "AWS::ApplicationAutoScaling::ScalingPolicy",
        ]

        models = {}
        for resource_type in resource_types:
            models[resource_type] = generate_resource_from_schema(resource_type)

        # Parse each resource with its corresponding model
        resources = ecs_alb_template["Resources"]

        # ECS Cluster
        cluster = models["AWS::ECS::Cluster"](**{"Type": "AWS::ECS::Cluster", **resources["ECSCluster"]})
        assert cluster.Type == "AWS::ECS::Cluster"
        assert cluster.Properties.ClusterName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-cluster"})

        # Security Groups
        alb_sg = models["AWS::EC2::SecurityGroup"](
            **{"Type": "AWS::EC2::SecurityGroup", **resources["ALBSecurityGroup"]}
        )
        assert alb_sg.Type == "AWS::EC2::SecurityGroup"
        assert alb_sg.Properties.VpcId == FunctionDict(Ref="VpcId")

        ecs_sg = models["AWS::EC2::SecurityGroup"](
            **{"Type": "AWS::EC2::SecurityGroup", **resources["ECSSecurityGroup"]}
        )
        assert ecs_sg.Type == "AWS::EC2::SecurityGroup"

        # ALB
        alb = models["AWS::ElasticLoadBalancingV2::LoadBalancer"](
            **{"Type": "AWS::ElasticLoadBalancingV2::LoadBalancer", **resources["ApplicationLoadBalancer"]}
        )
        assert alb.Type == "AWS::ElasticLoadBalancingV2::LoadBalancer"
        assert alb.Properties.Scheme == "internet-facing"

        # Target Group
        tg = models["AWS::ElasticLoadBalancingV2::TargetGroup"](
            **{"Type": "AWS::ElasticLoadBalancingV2::TargetGroup", **resources["TargetGroup"]}
        )
        assert tg.Type == "AWS::ElasticLoadBalancingV2::TargetGroup"
        assert tg.Properties.TargetType == "ip"
        assert tg.Properties.HealthCheckPath == "/health"

        # Listener
        listener = models["AWS::ElasticLoadBalancingV2::Listener"](
            **{"Type": "AWS::ElasticLoadBalancingV2::Listener", **resources["ALBListener"]}
        )
        assert listener.Type == "AWS::ElasticLoadBalancingV2::Listener"
        assert listener.Properties.Port == 80

        # IAM Roles
        exec_role = models["AWS::IAM::Role"](**{"Type": "AWS::IAM::Role", **resources["ECSTaskExecutionRole"]})
        assert exec_role.Type == "AWS::IAM::Role"

        task_role = models["AWS::IAM::Role"](**{"Type": "AWS::IAM::Role", **resources["ECSTaskRole"]})
        assert task_role.Type == "AWS::IAM::Role"

        # Log Group
        log_group = models["AWS::Logs::LogGroup"](**{"Type": "AWS::Logs::LogGroup", **resources["LogGroup"]})
        assert log_group.Type == "AWS::Logs::LogGroup"
        assert log_group.Properties.LogGroupName == FunctionDict(**{"Fn::Sub": "/ecs/${AWS::StackName}"})
        # Test Fn::If condition
        assert log_group.Properties.RetentionInDays == FunctionDict(**{"Fn::If": ["IsProd", 90, 14]})

        # Task Definition
        task_def = models["AWS::ECS::TaskDefinition"](
            **{"Type": "AWS::ECS::TaskDefinition", **resources["TaskDefinition"]}
        )
        assert task_def.Type == "AWS::ECS::TaskDefinition"
        assert task_def.Properties.NetworkMode == "awsvpc"
        # Test Fn::If for Cpu
        assert task_def.Properties.Cpu == FunctionDict(**{"Fn::If": ["IsProd", "1024", "256"]})

        # ECS Service
        service = models["AWS::ECS::Service"](**{"Type": "AWS::ECS::Service", **resources["ECSService"]})
        assert service.Type == "AWS::ECS::Service"
        assert service.DependsOn == ["ALBListener"]
        assert service.Properties.LaunchType == "FARGATE"

        # Auto Scaling (conditional resources)
        scaling_target = models["AWS::ApplicationAutoScaling::ScalableTarget"](
            **{"Type": "AWS::ApplicationAutoScaling::ScalableTarget", **resources["AutoScalingTarget"]}
        )
        assert scaling_target.Type == "AWS::ApplicationAutoScaling::ScalableTarget"
        assert scaling_target.Condition == "IsProd"
        assert scaling_target.Properties.MaxCapacity == 10

        scaling_policy = models["AWS::ApplicationAutoScaling::ScalingPolicy"](
            **{"Type": "AWS::ApplicationAutoScaling::ScalingPolicy", **resources["AutoScalingPolicy"]}
        )
        assert scaling_policy.Type == "AWS::ApplicationAutoScaling::ScalingPolicy"
        assert scaling_policy.Condition == "IsProd"

    def test_ecs_service_network_configuration(self, ecs_alb_template):
        """Test that complex nested properties like NetworkConfiguration are properly handled."""
        ECSService = generate_resource_from_schema("AWS::ECS::Service")

        service = ECSService(**{"Type": "AWS::ECS::Service", **ecs_alb_template["Resources"]["ECSService"]})

        # Verify nested NetworkConfiguration
        assert service.Properties.NetworkConfiguration is not None

    def test_task_definition_container_definitions(self, ecs_alb_template):
        """Test that array properties like ContainerDefinitions are properly handled."""
        TaskDefinition = generate_resource_from_schema("AWS::ECS::TaskDefinition")

        task_def = TaskDefinition(
            **{"Type": "AWS::ECS::TaskDefinition", **ecs_alb_template["Resources"]["TaskDefinition"]}
        )

        # Verify ContainerDefinitions is a list
        assert task_def.Properties.ContainerDefinitions is not None
        assert isinstance(task_def.Properties.ContainerDefinitions, list)

    def test_alb_listener_default_actions(self, ecs_alb_template):
        """Test that listener default actions with forward type are properly handled."""
        Listener = generate_resource_from_schema("AWS::ElasticLoadBalancingV2::Listener")

        listener = Listener(
            **{"Type": "AWS::ElasticLoadBalancingV2::Listener", **ecs_alb_template["Resources"]["ALBListener"]}
        )

        # Verify DefaultActions
        assert listener.Properties.DefaultActions is not None
        assert isinstance(listener.Properties.DefaultActions, list)

    def test_iam_role_assume_role_policy_document(self, ecs_alb_template):
        """Test that IAM Role AssumeRolePolicyDocument is properly handled."""
        IAMRole = generate_resource_from_schema("AWS::IAM::Role")

        role = IAMRole(**{"Type": "AWS::IAM::Role", **ecs_alb_template["Resources"]["ECSTaskExecutionRole"]})

        # Verify AssumeRolePolicyDocument
        assert role.Properties.AssumeRolePolicyDocument is not None

    def test_all_intrinsic_functions_in_template(self, ecs_alb_template):
        """Verify all intrinsic functions used in the template are properly parsed."""
        # Generate models for resources that use various intrinsic functions
        ECSCluster = generate_resource_from_schema("AWS::ECS::Cluster")
        LogGroup = generate_resource_from_schema("AWS::Logs::LogGroup")
        ScalableTarget = generate_resource_from_schema("AWS::ApplicationAutoScaling::ScalableTarget")

        # Fn::Sub
        cluster = ECSCluster(**{"Type": "AWS::ECS::Cluster", **ecs_alb_template["Resources"]["ECSCluster"]})
        assert cluster.Properties.ClusterName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-cluster"})

        # Fn::If
        log_group = LogGroup(**{"Type": "AWS::Logs::LogGroup", **ecs_alb_template["Resources"]["LogGroup"]})
        assert log_group.Properties.RetentionInDays == FunctionDict(**{"Fn::If": ["IsProd", 90, 14]})

        # Fn::Join with Ref and Fn::GetAtt
        scaling_target = ScalableTarget(
            **{
                "Type": "AWS::ApplicationAutoScaling::ScalableTarget",
                **ecs_alb_template["Resources"]["AutoScalingTarget"],
            }
        )
        expected_resource_id = FunctionDict(
            **{
                "Fn::Join": [
                    "/",
                    [
                        "service",
                        {"Ref": "ECSCluster"},
                        {"Fn::GetAtt": ["ECSService", "Name"]},
                    ],
                ]
            }
        )
        assert scaling_target.Properties.ResourceId == expected_resource_id
