"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
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
            "Outputs": {},
        }
    )


def test_basic_json(model):
    assert type(model).__name__ == "CFModel"
    assert len(model.Resources) == 1


def test_basic_yaml():
    pass


def test_resources_filtered_by_type():
    generic_resource = {"Logical ID": {"Type": "Resource type", "Properties": {"foo": "bar"}}}
    user = {"User": IAMUser()}

    model = CFModel(Resources={**generic_resource, **user})
    assert model.resources_filtered_by_type(("Resource type",)) == generic_resource
    assert model.resources_filtered_by_type(("Resource type", IAMUser)) == {**generic_resource, **user}
    assert model.resources_filtered_by_type((IAMUser,)) == user
