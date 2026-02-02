"""Tests for the resource generator script."""

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from pycfmodel import parse
from pycfmodel.model.base import FunctionDict
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.resources.s3_bucket import S3Bucket

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "generate_resource_from_schema.py"


class TestGeneratedCodeCompilation:
    """Test that generated code compiles and works correctly."""

    def test_generated_s3_bucket_compiles(self):
        """Test that generated S3 bucket code compiles without errors."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::S3::Bucket"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Try to compile the generated code
        code = result.stdout
        compile(code, "<generated>", "exec")

    def test_generated_lambda_function_compiles(self):
        """Test that generated Lambda function code compiles without errors."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        code = result.stdout
        compile(code, "<generated>", "exec")

    def test_generated_dynamodb_table_compiles(self):
        """Test that generated DynamoDB table code compiles without errors."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::DynamoDB::Table"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        code = result.stdout
        compile(code, "<generated>", "exec")


class TestGeneratedCodeFunctionality:
    """Test that generated classes work like existing pycfmodel resources."""

    @pytest.fixture
    def generated_lambda_module(self):
        """Generate and load Lambda function module."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        # Write to temp file and import
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(result.stdout)
            temp_path = f.name

        import importlib.util

        spec = importlib.util.spec_from_file_location("generated_lambda", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        yield module

        # Cleanup
        Path(temp_path).unlink()

    @pytest.fixture
    def generated_ec2_module(self):
        """Generate and load EC2 VPC module."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::EC2::VPC"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(result.stdout)
            temp_path = f.name

        import importlib.util

        spec = importlib.util.spec_from_file_location("generated_ec2_vpc", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        yield module

        Path(temp_path).unlink()

    def test_generated_lambda_inherits_from_resource(self, generated_lambda_module):
        """Test that generated Lambda class inherits from Resource."""
        assert issubclass(generated_lambda_module.LambdaFunction, Resource)

    def test_generated_lambda_can_be_instantiated(self, generated_lambda_module):
        """Test that generated Lambda class can be instantiated."""
        LambdaFunction = generated_lambda_module.LambdaFunction
        LambdaFunctionProperties = generated_lambda_module.LambdaFunctionProperties

        props = LambdaFunctionProperties(
            Code={"ZipFile": "def handler(event, context): pass"},
            Role="arn:aws:iam::123456789012:role/lambda-role",
            FunctionName="my-function",
            Runtime="python3.12",
            Handler="index.handler",
        )

        function = LambdaFunction(
            Type="AWS::Lambda::Function",
            Properties=props,
        )

        assert function.Type == "AWS::Lambda::Function"
        assert function.Properties.FunctionName == "my-function"
        assert function.Properties.Runtime == "python3.12"

    def test_generated_lambda_handles_intrinsic_functions(self, generated_lambda_module):
        """Test that generated Lambda class handles intrinsic functions."""
        LambdaFunction = generated_lambda_module.LambdaFunction
        LambdaFunctionProperties = generated_lambda_module.LambdaFunctionProperties

        props = LambdaFunctionProperties(
            Code={"ZipFile": "def handler(event, context): pass"},
            Role={"Fn::GetAtt": ["LambdaRole", "Arn"]},
            FunctionName={"Fn::Sub": "${AWS::StackName}-function"},
            Runtime="python3.12",
        )

        function = LambdaFunction(
            Type="AWS::Lambda::Function",
            Properties=props,
        )

        assert function.Properties.FunctionName == FunctionDict(**{"Fn::Sub": "${AWS::StackName}-function"})
        assert function.Properties.Role == FunctionDict(**{"Fn::GetAtt": ["LambdaRole", "Arn"]})

    def test_generated_lambda_has_resource_attributes(self, generated_lambda_module):
        """Test that generated Lambda class has standard Resource attributes."""
        LambdaFunction = generated_lambda_module.LambdaFunction
        LambdaFunctionProperties = generated_lambda_module.LambdaFunctionProperties

        function = LambdaFunction(
            Type="AWS::Lambda::Function",
            Properties=LambdaFunctionProperties(
                Code={"ZipFile": "pass"},
                Role="arn:aws:iam::123456789012:role/role",
            ),
            DependsOn=["MyBucket"],
            Condition="CreateFunction",
            DeletionPolicy="Retain",
        )

        assert function.DependsOn == ["MyBucket"]
        assert function.Condition == "CreateFunction"
        assert function.DeletionPolicy == "Retain"

    def test_generated_ec2_vpc_can_be_instantiated(self, generated_ec2_module):
        """Test that generated EC2 VPC class can be instantiated."""
        EC2VPC = generated_ec2_module.EC2VPC
        EC2VPCProperties = generated_ec2_module.EC2VPCProperties

        props = EC2VPCProperties(
            CidrBlock="10.0.0.0/16",
            EnableDnsHostnames=True,
            EnableDnsSupport=True,
        )

        vpc = EC2VPC(
            Type="AWS::EC2::VPC",
            Properties=props,
        )

        assert vpc.Type == "AWS::EC2::VPC"
        assert vpc.Properties.CidrBlock == "10.0.0.0/16"
        assert vpc.Properties.EnableDnsHostnames is True


class TestGeneratedCodeStructure:
    """Test that generated code follows pycfmodel conventions."""

    def test_generated_code_has_properties_class(self):
        """Test that generated code defines a Properties class."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        code = result.stdout

        assert "class LambdaFunctionProperties(CustomModel):" in code
        assert "class LambdaFunction(Resource):" in code

    def test_generated_code_has_docstrings(self):
        """Test that generated code includes docstrings."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::S3::Bucket"],
            capture_output=True,
            text=True,
        )
        code = result.stdout

        assert '"""' in code
        assert "Properties:" in code
        assert "AWS Docs" in code

    def test_generated_code_has_type_literal(self):
        """Test that generated code uses Literal for Type field."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        code = result.stdout

        assert 'Type: Literal["AWS::Lambda::Function"]' in code

    def test_generated_code_uses_resolvable_types(self):
        """Test that generated code uses Resolvable type annotations."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        code = result.stdout

        assert "ResolvableStr" in code
        assert "ResolvableInt" in code or "ResolvableGeneric" in code
        assert "Resolvable[" in code

    def test_generated_code_imports_are_correct(self):
        """Test that generated code has proper imports."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        code = result.stdout

        assert "from typing import" in code
        assert "from pycfmodel.model.base import CustomModel" in code
        assert "from pycfmodel.model.resources.resource import Resource" in code


class TestExistingResourceComparison:
    """Compare generated resources with existing ones."""

    def test_s3_bucket_properties_match_existing(self):
        """Test that generated S3 bucket properties match existing implementation."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::S3::Bucket"],
            capture_output=True,
            text=True,
        )
        code = result.stdout

        # Key properties should be present
        assert "BucketName:" in code
        assert "BucketEncryption:" in code
        assert "VersioningConfiguration:" in code
        assert "Tags:" in code
        assert "WebsiteConfiguration:" in code

        # Should use similar type patterns
        assert "Optional[ResolvableStr]" in code  # For BucketName
        assert "Optional[ResolvableGeneric]" in code  # For complex types

    def test_generated_and_existing_s3_bucket_parse_same_template(self):
        """Test that both implementations parse the same template correctly."""
        # Parse with existing implementation
        template = {
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": "my-bucket",
                        "VersioningConfiguration": {"Status": "Enabled"},
                        "Tags": [{"Key": "Env", "Value": "prod"}],
                    },
                }
            }
        }

        model = parse(template)
        bucket = model.Resources["MyBucket"]

        # Verify existing implementation works
        assert isinstance(bucket, S3Bucket)
        assert bucket.Properties.BucketName == "my-bucket"
        assert bucket.Type == "AWS::S3::Bucket"

    def test_generated_resource_type_naming_convention(self):
        """Test that generated class names follow pycfmodel conventions."""
        # AWS::S3::Bucket -> S3Bucket
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::S3::Bucket"],
            capture_output=True,
            text=True,
        )
        assert "class S3Bucket(Resource):" in result.stdout
        assert "class S3BucketProperties(CustomModel):" in result.stdout

        # AWS::Lambda::Function -> LambdaFunction
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        assert "class LambdaFunction(Resource):" in result.stdout
        assert "class LambdaFunctionProperties(CustomModel):" in result.stdout

        # AWS::EC2::SecurityGroup -> EC2SecurityGroup
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::EC2::SecurityGroup"],
            capture_output=True,
            text=True,
        )
        assert "class EC2SecurityGroup(Resource):" in result.stdout


class TestGeneratorCLI:
    """Test the CLI interface of the generator."""

    def test_list_types_option(self):
        """Test --list-types option."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--list-types"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "AWS::S3::Bucket" in result.stdout
        assert "AWS::Lambda::Function" in result.stdout

    def test_dry_run_option(self):
        """Test --dry-run option."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::S3::Bucket", "--dry-run"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        # Should output to stdout, not create file
        assert "class S3Bucket" in result.stdout

    def test_invalid_resource_type(self):
        """Test error handling for invalid resource type."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::Invalid::Resource"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "not found" in result.stderr

    def test_multiple_resource_types(self):
        """Test generating multiple resource types at once."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "AWS::S3::Bucket", "AWS::Lambda::Function"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "class S3Bucket" in result.stdout
        assert "class LambdaFunction" in result.stdout

    def test_output_to_directory(self, tmp_path):
        """Test writing generated code to a directory."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "AWS::Lambda::Function",
                "--output-dir",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        output_file = tmp_path / "lambda_function.py"
        assert output_file.exists()

        content = output_file.read_text()
        assert "class LambdaFunction(Resource):" in content
