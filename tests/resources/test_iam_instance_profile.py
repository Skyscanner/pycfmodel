import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.iam_instance_profile import IAMInstanceProfile


@pytest.fixture()
def valid_iam_instance_profile():
    return IAMInstanceProfile(
        **{
            "Type": "AWS::IAM::InstanceProfile",
            "Properties": {
                "InstanceProfileName": "my-instance-profile",
                "Path": "/",
                "Roles": ["my-ec2-role"],
            },
        }
    )


def test_valid_iam_instance_profile_resource(valid_iam_instance_profile):
    assert valid_iam_instance_profile.Properties.InstanceProfileName == "my-instance-profile"
    assert valid_iam_instance_profile.Properties.Path == "/"
    assert valid_iam_instance_profile.Properties.Roles == ["my-ec2-role"]


def test_iam_instance_profile_with_custom_path():
    profile = IAMInstanceProfile(
        **{
            "Type": "AWS::IAM::InstanceProfile",
            "Properties": {
                "InstanceProfileName": "my-instance-profile",
                "Path": "/application/",
                "Roles": ["my-ec2-role"],
            },
        }
    )
    assert profile.Properties.Path == "/application/"


def test_iam_instance_profile_minimal():
    profile = IAMInstanceProfile(
        **{
            "Type": "AWS::IAM::InstanceProfile",
            "Properties": {
                "Roles": ["my-role"],
            },
        }
    )
    assert profile.Properties.Roles == ["my-role"]
    assert profile.Properties.InstanceProfileName is None
    assert profile.Properties.Path is None


def test_iam_instance_profile_with_ref():
    from pycfmodel.model.base import FunctionDict

    profile = IAMInstanceProfile(
        **{
            "Type": "AWS::IAM::InstanceProfile",
            "Properties": {
                "InstanceProfileName": {"Fn::Sub": "${AWS::StackName}-instance-profile"},
                "Roles": [{"Ref": "EC2Role"}],
            },
        }
    )
    assert profile.Properties.Roles[0] == FunctionDict(**{"Ref": "EC2Role"})


def test_iam_instance_profile_requires_roles():
    with pytest.raises(ValidationError):
        IAMInstanceProfile(
            **{
                "Type": "AWS::IAM::InstanceProfile",
                "Properties": {
                    "InstanceProfileName": "my-instance-profile",
                },
            }
        )
