import pytest

from pycfmodel.model.cf_model import CFModel
from pycfmodel.model.generic import Generic
from pycfmodel.model.resources.generic_resource import GenericResource
from pycfmodel.model.resources.iam_user import IAMUser


@pytest.fixture()
def model():
    return CFModel(
        **{
            "AWSTemplateFormatVersion": "2012-12-12",
            "Description": "JSON string",
            "Metadata": {},
            "Parameters": {},
            "Mappings": {},
            "Conditions": {},
            "Transform": ["MyMacro", "AWS::Serverless"],
            "Resources": {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}},
            "Rules": {},
            "Outputs": {},
        }
    )


def test_basic_json(model: CFModel):
    assert type(model).__name__ == "CFModel"
    assert len(model.Resources) == 1
    assert model.Transform == ["MyMacro", "AWS::Serverless"]


def test_resources_filtered_by_type():
    generic_resource = {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}}
    user = {"User": IAMUser(Type="AWS::IAM::User")}

    model = CFModel(Resources={**generic_resource, **user})
    assert model.resources_filtered_by_type(("Resource type",)) == {
        "Logical ID": GenericResource(
            Type="Resource type",
            Condition=None,
            CreatePolicy=None,
            DeletionPolicy=None,
            DependsOn=None,
            Metadata=None,
            UpdatePolicy=None,
            UpdateReplacePolicy=None,
            Properties=Generic(foo="bar"),
        )
    }
    assert model.resources_filtered_by_type(("Resource type", IAMUser)) == {
        "Logical ID": GenericResource(
            Type="Resource type",
            Condition=None,
            CreatePolicy=None,
            DeletionPolicy=None,
            DependsOn=None,
            Metadata=None,
            UpdatePolicy=None,
            UpdateReplacePolicy=None,
            Properties=Generic(foo="bar"),
        ),
        "User": IAMUser(
            Type="AWS::IAM::User",
            Condition=None,
            CreatePolicy=None,
            DeletionPolicy=None,
            DependsOn=None,
            Metadata=None,
            UpdatePolicy=None,
            UpdateReplacePolicy=None,
            Properties=None,
        ),
    }
    assert model.resources_filtered_by_type((IAMUser,)) == user


def test_complex_metadata_schema():
    metadata = {"Foo": "a_string_value", "Bar": 1, "Fizz": ["a", "list"], "Buzz": {"another": "dict"}}

    model = CFModel(Metadata=metadata)
    assert model.Metadata == metadata


def test_backwards_compatible_metadata():
    metadata = {"ADict": {"foo": "bar"}}

    model = CFModel(Metadata=metadata)
    assert model.Metadata == metadata


def test_transform_handles_string():
    transform = "MyMacro"

    model = CFModel(Transform=transform)
    assert model.Transform == transform


def test_resolve_model(model):
    assert model.resolve() == model
