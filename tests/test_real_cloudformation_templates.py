"""Tests for parsing real CloudFormation YAML templates."""

from pathlib import Path

import pytest
import yaml

from pycfmodel import clear_dynamic_model_cache, disable_dynamic_generation, enable_dynamic_generation, parse
from pycfmodel.model.base import FunctionDict
from pycfmodel.model.resources.generic_resource import GenericResource
from pycfmodel.model.resources.iam_role import IAMRole
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.resources.s3_bucket import S3Bucket
from pycfmodel.model.resources.s3_bucket_policy import S3BucketPolicy
from pycfmodel.model.resources.security_group import SecurityGroup

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "cloudformation"


class CloudFormationLoader(yaml.SafeLoader):
    """Custom YAML loader that handles CloudFormation intrinsic functions."""

    pass


def _construct_cfn_tag(loader, tag_suffix, node):
    """Construct CloudFormation intrinsic function from YAML tag."""
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node, deep=True)
    elif isinstance(node, yaml.MappingNode):
        value = loader.construct_mapping(node, deep=True)
    else:
        value = None

    if tag_suffix == "Ref":
        return {"Ref": value}
    elif tag_suffix == "Condition":
        return {"Condition": value}
    elif tag_suffix == "GetAtt":
        # !GetAtt can be "Resource.Attribute" or [Resource, Attribute]
        if isinstance(value, str) and "." in value:
            return {"Fn::GetAtt": value.split(".", 1)}
        return {"Fn::GetAtt": value}
    else:
        return {f"Fn::{tag_suffix}": value}


# Register CloudFormation intrinsic function tags
CFN_TAGS = [
    "Ref",
    "Base64",
    "Cidr",
    "Condition",
    "Equals",
    "FindInMap",
    "GetAtt",
    "GetAZs",
    "If",
    "ImportValue",
    "Join",
    "Not",
    "Or",
    "And",
    "Select",
    "Split",
    "Sub",
    "Transform",
]

for tag in CFN_TAGS:
    CloudFormationLoader.add_constructor(
        f"!{tag}",
        lambda loader, node, tag=tag: _construct_cfn_tag(loader, tag, node),
    )


def load_yaml_template(filename: str) -> dict:
    """Load a YAML CloudFormation template from fixtures directory."""
    filepath = FIXTURES_DIR / filename
    with open(filepath) as f:
        return yaml.load(f, Loader=CloudFormationLoader)


@pytest.fixture(autouse=True)
def reset_dynamic_generation():
    """Reset dynamic generation state before and after each test."""
    disable_dynamic_generation()
    clear_dynamic_model_cache()
    yield
    disable_dynamic_generation()
    clear_dynamic_model_cache()


class TestS3StaticWebsiteTemplate:
    """Tests for s3_static_website.yaml template."""

    @pytest.fixture
    def template(self):
        return load_yaml_template("s3_static_website.yaml")

    def test_parse_without_dynamic_generation(self, template):
        """Parse S3 static website template without dynamic generation."""
        model = parse(template)

        # Verify template metadata
        assert model.AWSTemplateFormatVersion.isoformat() == "2010-09-09"
        assert model.Description == "S3 bucket configured for static website hosting"

        # Verify parameters
        assert "BucketName" in model.Parameters
        assert model.Parameters["BucketName"].Default == "my-static-website-bucket"
        assert "Environment" in model.Parameters
        assert model.Parameters["Environment"].AllowedValues == ["dev", "staging", "prod"]

        # Verify conditions
        assert "IsProd" in model.Conditions

        # Verify resources
        assert len(model.Resources) == 2

        # WebsiteBucket is explicitly modeled
        bucket = model.Resources["WebsiteBucket"]
        assert isinstance(bucket, S3Bucket)
        assert bucket.Type == "AWS::S3::Bucket"
        assert bucket.Properties.BucketName == FunctionDict(**{"Fn::Sub": "${BucketName}-${Environment}"})

        # BucketPolicy is explicitly modeled
        policy = model.Resources["BucketPolicy"]
        assert isinstance(policy, S3BucketPolicy)
        assert policy.Properties.Bucket == FunctionDict(**{"Ref": "WebsiteBucket"})

        # Verify outputs
        assert "BucketArn" in model.Outputs
        assert "WebsiteURL" in model.Outputs

    def test_resolve_template(self, template):
        """Test resolving the template with parameters."""
        model = parse(template)
        resolved = model.resolve({"BucketName": "test-bucket", "Environment": "prod"})

        # Verify bucket name is resolved
        bucket = resolved.Resources["WebsiteBucket"]
        assert bucket.Properties.BucketName == "test-bucket-prod"

        # Verify condition is resolved
        assert resolved.Conditions["IsProd"] is True


class TestLambdaApiGatewayTemplate:
    """Tests for lambda_api_gateway.yaml template."""

    @pytest.fixture
    def template(self):
        return load_yaml_template("lambda_api_gateway.yaml")

    def test_parse_without_dynamic_generation(self, template):
        """Parse Lambda API Gateway template - some resources become GenericResource."""
        model = parse(template)

        # Verify template metadata
        assert model.Description == "Lambda function with API Gateway REST API"

        # Verify parameters
        assert "FunctionName" in model.Parameters
        assert model.Parameters["MemorySize"].Default == 256
        assert model.Parameters["Timeout"].MaxValue == 900

        # LambdaExecutionRole is explicitly modeled
        role = model.Resources["LambdaExecutionRole"]
        assert isinstance(role, IAMRole)
        assert role.Properties.RoleName == FunctionDict(**{"Fn::Sub": "${FunctionName}-execution-role"})

        # LambdaFunction is NOT explicitly modeled (becomes GenericResource)
        lambda_fn = model.Resources["LambdaFunction"]
        assert isinstance(lambda_fn, GenericResource)
        assert lambda_fn.Type == "AWS::Lambda::Function"
        assert lambda_fn.DependsOn == ["LambdaExecutionRole"]

        # DynamoDB table is NOT explicitly modeled
        table = model.Resources["DataTable"]
        assert isinstance(table, GenericResource)
        assert table.Type == "AWS::DynamoDB::Table"

        # API Gateway resources are NOT explicitly modeled
        api = model.Resources["RestApi"]
        assert isinstance(api, GenericResource)
        assert api.Type == "AWS::ApiGateway::RestApi"

    def test_parse_with_dynamic_generation(self, template):
        """Parse Lambda API Gateway template with dynamic generation enabled."""
        enable_dynamic_generation()

        model = parse(template)

        # LambdaFunction should now be a typed resource
        lambda_fn = model.Resources["LambdaFunction"]
        assert not isinstance(lambda_fn, GenericResource)
        assert isinstance(lambda_fn, Resource)
        assert lambda_fn.Type == "AWS::Lambda::Function"
        assert lambda_fn.Properties.FunctionName == FunctionDict(**{"Ref": "FunctionName"})
        assert lambda_fn.Properties.Runtime == "python3.12"
        assert lambda_fn.Properties.MemorySize == FunctionDict(**{"Ref": "MemorySize"})
        assert lambda_fn.DependsOn == ["LambdaExecutionRole"]

        # DynamoDB table should be typed
        table = model.Resources["DataTable"]
        assert not isinstance(table, GenericResource)
        assert table.Type == "AWS::DynamoDB::Table"
        assert table.Properties.TableName == FunctionDict(**{"Fn::Sub": "${FunctionName}-data"})
        assert table.Properties.BillingMode == "PAY_PER_REQUEST"

        # API Gateway resources should be typed
        api = model.Resources["RestApi"]
        assert not isinstance(api, GenericResource)
        assert api.Type == "AWS::ApiGateway::RestApi"
        assert api.Properties.Name == FunctionDict(**{"Fn::Sub": "${FunctionName}-api"})

        # Lambda permission should be typed
        permission = model.Resources["LambdaPermission"]
        assert not isinstance(permission, GenericResource)
        assert permission.Type == "AWS::Lambda::Permission"
        assert permission.Properties.Action == "lambda:InvokeFunction"

        # IAM Role should still use explicit model
        role = model.Resources["LambdaExecutionRole"]
        assert isinstance(role, IAMRole)

    def test_resource_count(self, template):
        """Verify all resources are parsed."""
        model = parse(template)
        assert len(model.Resources) == 9

        expected_resources = [
            "LambdaExecutionRole",
            "LambdaFunction",
            "LambdaPermission",
            "DataTable",
            "RestApi",
            "ApiResource",
            "ApiMethod",
            "ApiDeployment",
            "ApiStage",
        ]
        for resource_name in expected_resources:
            assert resource_name in model.Resources


class TestEcsFargateServiceTemplate:
    """Tests for ecs_fargate_service.yaml template."""

    @pytest.fixture
    def template(self):
        return load_yaml_template("ecs_fargate_service.yaml")

    def test_parse_without_dynamic_generation(self, template):
        """Parse ECS Fargate template without dynamic generation."""
        model = parse(template)

        # Verify template metadata
        assert model.Description == "ECS Fargate service with ALB and auto-scaling"

        # Verify parameters
        assert "VpcId" in model.Parameters
        assert model.Parameters["DesiredCount"].Default == 2
        assert model.Parameters["ContainerImage"].Default == "nginx:latest"

        # Verify mappings
        assert "EnvironmentConfig" in model.Mappings
        assert model.Mappings["EnvironmentConfig"]["dev"]["Cpu"] == "256"
        assert model.Mappings["EnvironmentConfig"]["prod"]["Memory"] == "1024"

        # Verify conditions
        assert "HasMultipleTasks" in model.Conditions

        # Security groups are explicitly modeled
        alb_sg = model.Resources["ALBSecurityGroup"]
        assert isinstance(alb_sg, SecurityGroup)
        assert alb_sg.Properties.GroupDescription == "Security group for ALB"

        service_sg = model.Resources["ServiceSecurityGroup"]
        assert isinstance(service_sg, SecurityGroup)

        # IAM Roles are explicitly modeled
        execution_role = model.Resources["TaskExecutionRole"]
        assert isinstance(execution_role, IAMRole)

        # ECS resources are NOT explicitly modeled
        cluster = model.Resources["ECSCluster"]
        assert isinstance(cluster, GenericResource)
        assert cluster.Type == "AWS::ECS::Cluster"

        task_def = model.Resources["TaskDefinition"]
        assert isinstance(task_def, GenericResource)
        assert task_def.Type == "AWS::ECS::TaskDefinition"

        # ALB resources are NOT explicitly modeled
        alb = model.Resources["LoadBalancer"]
        assert isinstance(alb, GenericResource)
        assert alb.Type == "AWS::ElasticLoadBalancingV2::LoadBalancer"

    def test_parse_with_dynamic_generation(self, template):
        """Parse ECS Fargate template with dynamic generation enabled."""
        enable_dynamic_generation()

        model = parse(template)

        # ECS Cluster should be typed
        cluster = model.Resources["ECSCluster"]
        assert not isinstance(cluster, GenericResource)
        assert cluster.Type == "AWS::ECS::Cluster"
        assert cluster.Properties.ClusterName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-cluster"})

        # Task Definition should be typed
        task_def = model.Resources["TaskDefinition"]
        assert not isinstance(task_def, GenericResource)
        assert task_def.Type == "AWS::ECS::TaskDefinition"
        assert task_def.Properties.NetworkMode == "awsvpc"
        assert task_def.Properties.RequiresCompatibilities == ["FARGATE"]

        # ECS Service should be typed with DependsOn
        service = model.Resources["ECSService"]
        assert not isinstance(service, GenericResource)
        assert service.Type == "AWS::ECS::Service"
        assert service.DependsOn == ["Listener"]

        # ALB should be typed
        alb = model.Resources["LoadBalancer"]
        assert not isinstance(alb, GenericResource)
        assert alb.Type == "AWS::ElasticLoadBalancingV2::LoadBalancer"
        assert alb.Properties.Scheme == "internet-facing"

        # Target Group should be typed
        tg = model.Resources["TargetGroup"]
        assert not isinstance(tg, GenericResource)
        assert tg.Type == "AWS::ElasticLoadBalancingV2::TargetGroup"
        assert tg.Properties.TargetType == "ip"

        # CloudWatch Log Group should be typed
        log_group = model.Resources["LogGroup"]
        assert not isinstance(log_group, GenericResource)
        assert log_group.Type == "AWS::Logs::LogGroup"
        assert log_group.Properties.RetentionInDays == 30

        # Auto Scaling resources should be typed (with Condition)
        scalable_target = model.Resources["ScalableTarget"]
        assert not isinstance(scalable_target, GenericResource)
        assert scalable_target.Type == "AWS::ApplicationAutoScaling::ScalableTarget"
        assert scalable_target.Condition == "HasMultipleTasks"

        # Security groups should still use explicit model
        alb_sg = model.Resources["ALBSecurityGroup"]
        assert isinstance(alb_sg, SecurityGroup)

    def test_intrinsic_functions_preserved(self, template):
        """Verify intrinsic functions are preserved during parsing."""
        enable_dynamic_generation()

        model = parse(template)

        # Check Fn::Sub
        cluster = model.Resources["ECSCluster"]
        assert cluster.Properties.ClusterName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-cluster"})

        # Check Fn::FindInMap
        task_def = model.Resources["TaskDefinition"]
        assert task_def.Properties.Cpu == FunctionDict(
            **{"Fn::FindInMap": ["EnvironmentConfig", "dev", "Cpu"]}
        )

        # Check Fn::GetAtt
        assert task_def.Properties.ExecutionRoleArn == FunctionDict(
            **{"Fn::GetAtt": ["TaskExecutionRole", "Arn"]}
        )

        # Check Fn::Ref
        service = model.Resources["ECSService"]
        assert service.Properties.Cluster == FunctionDict(**{"Ref": "ECSCluster"})


class TestVpcNetworkTemplate:
    """Tests for vpc_network.yaml template."""

    @pytest.fixture
    def template(self):
        return load_yaml_template("vpc_network.yaml")

    def test_parse_without_dynamic_generation(self, template):
        """Parse VPC network template without dynamic generation."""
        model = parse(template)

        # Verify template metadata
        assert model.Description == "VPC with public and private subnets, NAT Gateway, and VPC endpoints"

        # Verify parameters
        assert "VpcCidr" in model.Parameters
        assert model.Parameters["VpcCidr"].Default == "10.0.0.0/16"
        assert model.Parameters["EnableNatGateway"].AllowedValues == ["true", "false"]

        # Verify conditions (Fn::Equals, Fn::And, Fn::Not)
        assert "CreateNatGateway" in model.Conditions
        assert "IsProdEnvironment" in model.Conditions
        assert "CreateNatGatewayInProd" in model.Conditions

        # IAM Role is explicitly modeled
        flow_log_role = model.Resources["FlowLogRole"]
        assert isinstance(flow_log_role, IAMRole)
        assert flow_log_role.Condition == "IsProdEnvironment"

        # VPC resources are NOT explicitly modeled
        vpc = model.Resources["VPC"]
        assert isinstance(vpc, GenericResource)
        assert vpc.Type == "AWS::EC2::VPC"

        # Subnet resources are NOT explicitly modeled
        public_subnet = model.Resources["PublicSubnet1"]
        assert isinstance(public_subnet, GenericResource)
        assert public_subnet.Type == "AWS::EC2::Subnet"

    def test_parse_with_dynamic_generation(self, template):
        """Parse VPC network template with dynamic generation enabled."""
        enable_dynamic_generation()

        model = parse(template)

        # VPC should be typed
        vpc = model.Resources["VPC"]
        assert not isinstance(vpc, GenericResource)
        assert vpc.Type == "AWS::EC2::VPC"
        assert vpc.Properties.CidrBlock == FunctionDict(**{"Ref": "VpcCidr"})
        assert vpc.Properties.EnableDnsHostnames is True

        # Subnets should be typed
        public_subnet = model.Resources["PublicSubnet1"]
        assert not isinstance(public_subnet, GenericResource)
        assert public_subnet.Type == "AWS::EC2::Subnet"
        assert public_subnet.Properties.MapPublicIpOnLaunch is True

        private_subnet = model.Resources["PrivateSubnet1"]
        assert not isinstance(private_subnet, GenericResource)
        assert private_subnet.Type == "AWS::EC2::Subnet"

        # Internet Gateway should be typed
        igw = model.Resources["InternetGateway"]
        assert not isinstance(igw, GenericResource)
        assert igw.Type == "AWS::EC2::InternetGateway"

        # NAT Gateway should be typed with Condition
        nat = model.Resources["NatGateway"]
        assert not isinstance(nat, GenericResource)
        assert nat.Type == "AWS::EC2::NatGateway"
        assert nat.Condition == "CreateNatGateway"

        # Route Table should be typed
        rt = model.Resources["PublicRouteTable"]
        assert not isinstance(rt, GenericResource)
        assert rt.Type == "AWS::EC2::RouteTable"

        # VPC Endpoint should be typed
        endpoint = model.Resources["S3Endpoint"]
        assert not isinstance(endpoint, GenericResource)
        assert endpoint.Type == "AWS::EC2::VPCEndpoint"
        assert endpoint.Properties.VpcEndpointType == "Gateway"

        # Flow Log should be typed with Condition
        flow_log = model.Resources["VPCFlowLog"]
        assert not isinstance(flow_log, GenericResource)
        assert flow_log.Type == "AWS::EC2::FlowLog"
        assert flow_log.Condition == "IsProdEnvironment"
        assert flow_log.Properties.TrafficType == "ALL"

    def test_complex_intrinsic_functions(self, template):
        """Test complex intrinsic function combinations."""
        enable_dynamic_generation()

        model = parse(template)

        # Check Fn::Select with Fn::Cidr and Fn::Ref
        subnet = model.Resources["PublicSubnet1"]
        assert subnet.Properties.CidrBlock == FunctionDict(
            **{"Fn::Select": [0, {"Fn::Cidr": [{"Ref": "VpcCidr"}, 6, 8]}]}
        )

        # Check Fn::Select with Fn::GetAZs
        assert subnet.Properties.AvailabilityZone == FunctionDict(
            **{"Fn::Select": [0, {"Fn::GetAZs": ""}]}
        )

        # Check Fn::Sub with pseudo parameters
        endpoint = model.Resources["S3Endpoint"]
        assert endpoint.Properties.ServiceName == FunctionDict(
            **{"Fn::Sub": "com.amazonaws.${AWS::Region}.s3"}
        )

    def test_conditions_parsed_correctly(self, template):
        """Test that conditions are correctly parsed from the template."""
        model = parse(template)

        # Verify conditions are parsed (complex functions like Fn::Cidr can't be resolved)
        assert "CreateNatGateway" in model.Conditions
        assert "IsProdEnvironment" in model.Conditions
        assert "CreateNatGatewayInProd" in model.Conditions

        # Check condition structure - Fn::Equals
        assert model.Conditions["CreateNatGateway"] == {"Fn::Equals": [{"Ref": "EnableNatGateway"}, "true"]}
        assert model.Conditions["IsProdEnvironment"] == {"Fn::Equals": [{"Ref": "Environment"}, "prod"]}

        # Check Fn::And condition
        assert model.Conditions["CreateNatGatewayInProd"]["Fn::And"] is not None

        # Verify resources with conditions have Condition attribute set
        nat_gateway = model.Resources["NatGateway"]
        assert nat_gateway.Condition == "CreateNatGateway"

        flow_log = model.Resources["VPCFlowLog"]
        assert flow_log.Condition == "IsProdEnvironment"

        flow_log_role = model.Resources["FlowLogRole"]
        assert flow_log_role.Condition == "IsProdEnvironment"

    def test_resource_count(self, template):
        """Verify all resources are parsed."""
        model = parse(template)

        # Count expected resources
        expected_count = 21  # VPC, IGW, attachment, 4 subnets, EIP, NAT, 2 route tables, etc.
        assert len(model.Resources) == expected_count


class TestOutputVerification:
    """Tests for verifying outputs are correctly parsed."""

    def test_s3_outputs(self):
        template = load_yaml_template("s3_static_website.yaml")
        model = parse(template)

        assert len(model.Outputs) == 2
        assert "BucketArn" in model.Outputs
        assert "WebsiteURL" in model.Outputs

        assert model.Outputs["BucketArn"]["Description"] == "ARN of the S3 bucket"
        assert model.Outputs["BucketArn"]["Value"] == {"Fn::GetAtt": ["WebsiteBucket", "Arn"]}

    def test_lambda_outputs(self):
        template = load_yaml_template("lambda_api_gateway.yaml")
        model = parse(template)

        assert len(model.Outputs) == 3
        assert "ApiEndpoint" in model.Outputs
        assert "LambdaFunctionArn" in model.Outputs
        assert "TableName" in model.Outputs

    def test_vpc_outputs_with_exports(self):
        template = load_yaml_template("vpc_network.yaml")
        model = parse(template)

        assert "VpcId" in model.Outputs
        assert "Export" in model.Outputs["VpcId"]
        assert model.Outputs["VpcId"]["Export"]["Name"] == {"Fn::Sub": "${AWS::StackName}-VpcId"}

        # Conditional output
        assert "NatGatewayId" in model.Outputs


class TestMappingsVerification:
    """Tests for verifying mappings are correctly parsed."""

    def test_ecs_mappings(self):
        template = load_yaml_template("ecs_fargate_service.yaml")
        model = parse(template)

        assert "EnvironmentConfig" in model.Mappings
        assert model.Mappings["EnvironmentConfig"]["dev"]["Cpu"] == "256"
        assert model.Mappings["EnvironmentConfig"]["dev"]["Memory"] == "512"
        assert model.Mappings["EnvironmentConfig"]["prod"]["Cpu"] == "512"
        assert model.Mappings["EnvironmentConfig"]["prod"]["Memory"] == "1024"
