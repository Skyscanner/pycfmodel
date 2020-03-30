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
            "Transform": [],
            "Resources": {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}},
            "Rules": {},
            "Outputs": {},
        }
    )


def test_basic_json(model):
    assert type(model).__name__ == "CFModel"
    assert len(model.Resources) == 1


def test_resources_filtered_by_type():
    generic_resource = {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}}
    user = {"User": IAMUser()}

    model = CFModel(Resources={**generic_resource, **user})
    assert model.resources_filtered_by_type(("Resource type",)) == generic_resource
    assert model.resources_filtered_by_type(("Resource type", IAMUser)) == {**generic_resource, **user}
    assert model.resources_filtered_by_type((IAMUser,)) == user
