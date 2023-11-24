import pytest

from pycfmodel.model.cf_model import CFModel
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
            "Globals": {},
        }
    )


@pytest.fixture()
def model_single_transform():
    return CFModel(
        **{
            "AWSTemplateFormatVersion": "2012-12-12",
            "Description": "",
            "Metadata": {},
            "Parameters": {},
            "Mappings": {},
            "Conditions": {},
            "Transform": "AWS::Serverless-2016-10-31",
            "Resources": {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}},
            "Rules": {},
            "Outputs": {},
        }
    )


@pytest.fixture()
def model_no_transform():
    return CFModel(
        **{
            "AWSTemplateFormatVersion": "2012-12-12",
            "Description": "",
            "Metadata": {},
            "Parameters": {},
            "Mappings": {},
            "Conditions": {},
            "Resources": {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}},
            "Rules": {},
            "Outputs": {},
        }
    )


@pytest.fixture()
def model_with_empty_globals():
    return CFModel(
        **{
            "AWSTemplateFormatVersion": "2012-12-12",
            "Globals": {},
            "Parameters": {},
            "Transform": "AWS::Serverless-2016-10-31",
            "Resources": {"Logical ID": {"Type": "AWS::Dummy::Dummy", "Properties": {"foo": "bar"}}},
        }
    )


def test_basic_json(model: CFModel):
    assert type(model).__name__ == "CFModel"
    assert len(model.Resources) == 1
    assert model.Transform == ["MyMacro", "AWS::Serverless"]
    assert model.Globals == {}


def test_resources_filtered_by_type():
    generic_resource = {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}}
    user = {"User": IAMUser()}

    model = CFModel(Resources={**generic_resource, **user})
    assert model.resources_filtered_by_type(("Resource type",)) == generic_resource
    assert model.resources_filtered_by_type(("Resource type", IAMUser)) == {**generic_resource, **user}
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


@pytest.mark.parametrize(
    "model_fixture,is_sam_model",
    [("model", True), ("model_single_transform", True), ("model_no_transform", False)],
)
def test_transform_is_of_type_sam_model(model_fixture, is_sam_model, request):
    assert request.getfixturevalue(model_fixture).is_sam_model() is is_sam_model


def test_model_with_empty_globals_is_able_to_resolve_to_empty_dict(model_with_empty_globals):
    assert model_with_empty_globals.Globals == {}
