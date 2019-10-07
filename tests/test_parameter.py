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

from pycfmodel.model.parameter import Parameter


@pytest.mark.parametrize(
    "param, expected",
    [
        ({"Type": "String", "NoEcho": True, "Default": "A"}, Parameter.NO_ECHO_WITH_DEFAULT),
        ({"Type": "String", "NoEcho": True}, Parameter.NO_ECHO_NO_DEFAULT),
        ({"Type": "String", "NoEcho": False, "Default": "A"}, "A"),
        ({"Type": "String", "NoEcho": False}, None),
        ({"Type": "String", "Default": "abc"}, "abc"),
        ({"Type": "String", "Default": None}, None),
        ({"Type": "Number", "Default": 1}, "1"),
        ({"Type": "List<Number>", "Default": "1,2,3"}, ["1", "2", "3"]),
        ({"Type": "CommaDelimitedList", "Default": "a,b,c"}, ["a", "b", "c"]),
    ],
)
def test_get_ref_value(param, expected):
    parameter = Parameter(**param)
    assert parameter.get_ref_value() == expected
