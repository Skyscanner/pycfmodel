"""
Copyright 2018 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


import pycfmodel

basic_template = {
    "AWSTemplateFormatVersion": "version date",

    "Description": "JSON string",

    "Metadata": {
    },

    "Parameters": {
    },

    "Mappings": {
    },

    "Conditions": {
    },

    "Transform": {
    },

    "Resources": {
        "Logical ID": {
            "Type": "Resource type",
            "Properties": {
                "foo": "bar"
            }
        }
    },

    "Outputs": {
    }
}


def test_basic_json():
    model = pycfmodel.parse(basic_template)

    assert type(model).__name__ == "CFModel"
    assert len(model.resources) == 1


def test_basic_yaml():
    pass
