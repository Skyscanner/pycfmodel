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

from pycfmodel.constants import IMPLEMENTED_FUNCTIONS
from pycfmodel.resolver import FUNCTION_MAPPINGS
from pycfmodel.utils import is_conditional_dict


def test_implemented_functions():
    assert set(FUNCTION_MAPPINGS) == IMPLEMENTED_FUNCTIONS


@pytest.mark.parametrize(
    "condition, expected_output",
    [
        ({"ArnEquals": ""}, True),
        ({"ForAllValues:ArnLike": ""}, True),
        ({"ArnEquals": "", "ForAllValues:ArnLike": ""}, True),
        ({"ArnEquals": "", "patata": ""}, False),
        ({"ForAllValues:ArnLike": "", "patata": ""}, False),
    ],
)
def test_is_conditional_dict(condition, expected_output):
    assert is_conditional_dict(condition) == expected_output
