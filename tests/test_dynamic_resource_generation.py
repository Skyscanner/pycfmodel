"""Tests for dynamic resource generation during template parsing."""

import pytest

from pycfmodel import (
    clear_dynamic_model_cache,
    disable_dynamic_generation,
    enable_dynamic_generation,
    is_dynamic_generation_enabled,
    parse,
)
from pycfmodel.model.resources.generic_resource import GenericResource
from pycfmodel.model.resources.resource import Resource


@pytest.fixture(autouse=True)
def reset_dynamic_generation():
    """Reset dynamic generation state before and after each test."""
    disable_dynamic_generation()
    clear_dynamic_model_cache()
    yield
    disable_dynamic_generation()
    clear_dynamic_model_cache()


class TestDynamicGenerationToggle:
    def test_dynamic_generation_disabled_by_default(self):
        assert is_dynamic_generation_enabled() is False

    def test_enable_dynamic_generation(self):
        enable_dynamic_generation()
        assert is_dynamic_generation_enabled() is True

    def test_disable_dynamic_generation(self):
        enable_dynamic_generation()
        disable_dynamic_generation()
        assert is_dynamic_generation_enabled() is False


class TestParseWithoutDynamicGeneration:
    def test_unmodeled_resource_becomes_generic_resource(self):
        """Without dynamic generation, unmodeled resources become GenericResource."""
        template = {
            "Resources": {
                "MyFunction": {
                    "Type": "AWS::Lambda::Function",
                    "Properties": {
                        "FunctionName": "my-function",
                        "Runtime": "python3.12",
                        "Role": "arn:aws:iam::123456789012:role/lambda-role",
                        "Code": {"ZipFile": "def handler(event, context): pass"},
                    },
                }
            }
        }

        model = parse(template)
        resource = model.Resources["MyFunction"]

        # Without dynamic generation, Lambda functions become GenericResource
        assert isinstance(resource, GenericResource)


class TestParseWithDynamicGeneration:
    def test_unmodeled_resource_becomes_typed_resource(self):
        """With dynamic generation, unmodeled resources get proper typed models."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyFunction": {
                    "Type": "AWS::Lambda::Function",
                    "Properties": {
                        "FunctionName": "my-function",
                        "Runtime": "python3.12",
                        "Role": "arn:aws:iam::123456789012:role/lambda-role",
                        "Code": {"ZipFile": "def handler(event, context): pass"},
                    },
                }
            }
        }

        model = parse(template)
        resource = model.Resources["MyFunction"]

        # With dynamic generation, Lambda function gets a typed model
        assert not isinstance(resource, GenericResource)
        assert isinstance(resource, Resource)
        assert resource.Type == "AWS::Lambda::Function"
        assert resource.Properties.FunctionName == "my-function"
        assert resource.Properties.Runtime == "python3.12"

    def test_explicitly_modeled_resource_still_uses_explicit_model(self):
        """Explicitly modeled resources should still use their explicit models."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": "my-bucket",
                    },
                }
            }
        }

        model = parse(template)
        resource = model.Resources["MyBucket"]

        # S3Bucket is explicitly modeled, should use that model
        from pycfmodel.model.resources.s3_bucket import S3Bucket

        assert isinstance(resource, S3Bucket)

    def test_mixed_resources_explicit_and_dynamic(self):
        """Template with both explicitly modeled and dynamically generated resources."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {"BucketName": "my-bucket"},
                },
                "MyFunction": {
                    "Type": "AWS::Lambda::Function",
                    "Properties": {
                        "FunctionName": "my-function",
                        "Runtime": "python3.12",
                        "Role": "arn:aws:iam::123456789012:role/lambda-role",
                        "Code": {"ZipFile": "def handler(event, context): pass"},
                    },
                },
                "MyQueue": {
                    "Type": "AWS::SQS::Queue",
                    "Properties": {"QueueName": "my-queue"},
                },
            }
        }

        model = parse(template)

        # S3Bucket - explicitly modeled
        from pycfmodel.model.resources.s3_bucket import S3Bucket

        assert isinstance(model.Resources["MyBucket"], S3Bucket)

        # Lambda Function - dynamically generated
        assert not isinstance(model.Resources["MyFunction"], GenericResource)
        assert model.Resources["MyFunction"].Type == "AWS::Lambda::Function"

        # SQS Queue - dynamically generated
        assert not isinstance(model.Resources["MyQueue"], GenericResource)
        assert model.Resources["MyQueue"].Type == "AWS::SQS::Queue"

    def test_ecs_cluster_dynamically_generated(self):
        """Test that ECS Cluster can be dynamically generated."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyCluster": {
                    "Type": "AWS::ECS::Cluster",
                    "Properties": {
                        "ClusterName": "my-cluster",
                        "ClusterSettings": [{"Name": "containerInsights", "Value": "enabled"}],
                    },
                }
            }
        }

        model = parse(template)
        resource = model.Resources["MyCluster"]

        assert not isinstance(resource, GenericResource)
        assert resource.Type == "AWS::ECS::Cluster"
        assert resource.Properties.ClusterName == "my-cluster"

    def test_dynamodb_table_dynamically_generated(self):
        """Test that DynamoDB Table can be dynamically generated."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyTable": {
                    "Type": "AWS::DynamoDB::Table",
                    "Properties": {
                        "TableName": "my-table",
                        "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
                        "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
                        "BillingMode": "PAY_PER_REQUEST",
                    },
                }
            }
        }

        model = parse(template)
        resource = model.Resources["MyTable"]

        assert not isinstance(resource, GenericResource)
        assert resource.Type == "AWS::DynamoDB::Table"
        assert resource.Properties.TableName == "my-table"

    def test_intrinsic_functions_work_with_dynamic_resources(self):
        """Test that intrinsic functions are properly handled in dynamic resources."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyFunction": {
                    "Type": "AWS::Lambda::Function",
                    "Properties": {
                        "FunctionName": {"Fn::Sub": "${AWS::StackName}-function"},
                        "Runtime": "python3.12",
                        "Role": {"Fn::GetAtt": ["LambdaRole", "Arn"]},
                        "Code": {"ZipFile": "def handler(event, context): pass"},
                    },
                }
            }
        }

        model = parse(template)
        resource = model.Resources["MyFunction"]

        assert not isinstance(resource, GenericResource)
        from pycfmodel.model.base import FunctionDict

        assert resource.Properties.FunctionName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-function"})
        assert resource.Properties.Role == FunctionDict(**{"Fn::GetAtt": ["LambdaRole", "Arn"]})

    def test_resource_with_condition(self):
        """Test that conditional resources work with dynamic generation."""
        enable_dynamic_generation()

        template = {
            "Conditions": {"CreateFunction": {"Fn::Equals": ["true", "true"]}},
            "Resources": {
                "MyFunction": {
                    "Type": "AWS::Lambda::Function",
                    "Condition": "CreateFunction",
                    "Properties": {
                        "FunctionName": "my-function",
                        "Runtime": "python3.12",
                        "Role": "arn:aws:iam::123456789012:role/lambda-role",
                        "Code": {"ZipFile": "def handler(event, context): pass"},
                    },
                }
            },
        }

        model = parse(template)
        resource = model.Resources["MyFunction"]

        assert not isinstance(resource, GenericResource)
        assert resource.Condition == "CreateFunction"

    def test_resource_with_depends_on(self):
        """Test that DependsOn works with dynamic generation."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {"BucketName": "my-bucket"},
                },
                "MyFunction": {
                    "Type": "AWS::Lambda::Function",
                    "DependsOn": ["MyBucket"],
                    "Properties": {
                        "FunctionName": "my-function",
                        "Runtime": "python3.12",
                        "Role": "arn:aws:iam::123456789012:role/lambda-role",
                        "Code": {"ZipFile": "def handler(event, context): pass"},
                    },
                },
            }
        }

        model = parse(template)
        resource = model.Resources["MyFunction"]

        assert not isinstance(resource, GenericResource)
        assert resource.DependsOn == ["MyBucket"]

    def test_unknown_resource_type_falls_back_to_generic(self):
        """Test that unknown resource types still fall back to GenericResource."""
        enable_dynamic_generation()

        template = {
            "Resources": {
                "MyCustomResource": {
                    "Type": "Custom::MyCustomType",
                    "Properties": {"Foo": "bar"},
                }
            }
        }

        model = parse(template)
        resource = model.Resources["MyCustomResource"]

        # Custom resources aren't in AWS schema, should fall back to GenericResource
        assert isinstance(resource, GenericResource)


class TestDynamicModelCaching:
    def test_models_are_cached(self):
        """Test that dynamically generated models are cached."""
        enable_dynamic_generation()

        from pycfmodel.model.resources.dynamic_resource import _dynamic_model_cache, get_or_create_dynamic_model

        # Clear cache first
        clear_dynamic_model_cache()
        assert len(_dynamic_model_cache) == 0

        # Generate a model
        model1 = get_or_create_dynamic_model("AWS::Lambda::Function")
        assert model1 is not None
        assert "AWS::Lambda::Function" in _dynamic_model_cache

        # Get the same model again - should be from cache
        model2 = get_or_create_dynamic_model("AWS::Lambda::Function")
        assert model2 is model1  # Same object from cache

    def test_clear_cache(self):
        """Test that cache can be cleared."""
        enable_dynamic_generation()

        from pycfmodel.model.resources.dynamic_resource import _dynamic_model_cache, get_or_create_dynamic_model

        get_or_create_dynamic_model("AWS::Lambda::Function")
        assert len(_dynamic_model_cache) > 0

        clear_dynamic_model_cache()
        assert len(_dynamic_model_cache) == 0


class TestComplexTemplate:
    def test_ecs_alb_template_with_dynamic_generation(self):
        """Test a complex ECS+ALB template with dynamic generation."""
        enable_dynamic_generation()

        template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "ECS with ALB",
            "Resources": {
                # Explicitly modeled
                "ALBSecurityGroup": {
                    "Type": "AWS::EC2::SecurityGroup",
                    "Properties": {
                        "GroupDescription": "ALB Security Group",
                        "VpcId": "vpc-12345",
                        "SecurityGroupIngress": [
                            {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "CidrIp": "0.0.0.0/0"}
                        ],
                    },
                },
                # Dynamically generated
                "ECSCluster": {
                    "Type": "AWS::ECS::Cluster",
                    "Properties": {"ClusterName": "my-cluster"},
                },
                "ALB": {
                    "Type": "AWS::ElasticLoadBalancingV2::LoadBalancer",
                    "Properties": {
                        "Name": "my-alb",
                        "Scheme": "internet-facing",
                        "Type": "application",
                        "Subnets": ["subnet-1", "subnet-2"],
                        "SecurityGroups": [{"Ref": "ALBSecurityGroup"}],
                    },
                },
                "TargetGroup": {
                    "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
                    "Properties": {
                        "Name": "my-tg",
                        "Port": 80,
                        "Protocol": "HTTP",
                        "VpcId": "vpc-12345",
                        "TargetType": "ip",
                    },
                },
                "TaskDefinition": {
                    "Type": "AWS::ECS::TaskDefinition",
                    "Properties": {
                        "Family": "my-task",
                        "NetworkMode": "awsvpc",
                        "RequiresCompatibilities": ["FARGATE"],
                        "Cpu": "256",
                        "Memory": "512",
                        "ContainerDefinitions": [
                            {
                                "Name": "app",
                                "Image": "nginx:latest",
                                "Essential": True,
                                "PortMappings": [{"ContainerPort": 80}],
                            }
                        ],
                    },
                },
                "ECSService": {
                    "Type": "AWS::ECS::Service",
                    "DependsOn": ["ALB"],
                    "Properties": {
                        "ServiceName": "my-service",
                        "Cluster": {"Ref": "ECSCluster"},
                        "TaskDefinition": {"Ref": "TaskDefinition"},
                        "DesiredCount": 2,
                        "LaunchType": "FARGATE",
                    },
                },
            },
        }

        model = parse(template)

        # Check explicitly modeled resource
        from pycfmodel.model.resources.security_group import SecurityGroup

        assert isinstance(model.Resources["ALBSecurityGroup"], SecurityGroup)

        # Check dynamically generated resources
        assert not isinstance(model.Resources["ECSCluster"], GenericResource)
        assert model.Resources["ECSCluster"].Type == "AWS::ECS::Cluster"

        assert not isinstance(model.Resources["ALB"], GenericResource)
        assert model.Resources["ALB"].Type == "AWS::ElasticLoadBalancingV2::LoadBalancer"

        assert not isinstance(model.Resources["TargetGroup"], GenericResource)
        assert model.Resources["TargetGroup"].Type == "AWS::ElasticLoadBalancingV2::TargetGroup"

        assert not isinstance(model.Resources["TaskDefinition"], GenericResource)
        assert model.Resources["TaskDefinition"].Type == "AWS::ECS::TaskDefinition"

        assert not isinstance(model.Resources["ECSService"], GenericResource)
        assert model.Resources["ECSService"].Type == "AWS::ECS::Service"
        assert model.Resources["ECSService"].DependsOn == ["ALB"]
