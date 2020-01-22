"""
Copyright 2018-2020 Skyscanner Ltd

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
    "param, provided_value, expected",
    [
        ({"Type": "String", "NoEcho": True, "Default": "A"}, None, Parameter.NO_ECHO_WITH_DEFAULT),
        ({"Type": "String", "NoEcho": True}, None, Parameter.NO_ECHO_NO_DEFAULT),
        ({"Type": "String", "NoEcho": False, "Default": "A"}, None, "A"),
        ({"Type": "String", "NoEcho": False}, None, None),
        ({"Type": "String", "Default": "abc"}, None, "abc"),
        ({"Type": "String", "Default": None}, None, None),
        ({"Type": "Number", "Default": 1}, None, "1"),
        ({"Type": "List<Number>", "Default": "1,2,3"}, None, ["1", "2", "3"]),
        ({"Type": "CommaDelimitedList", "Default": "a,b,c"}, None, ["a", "b", "c"]),
        # Tests with provided value
        ({"Type": "String", "NoEcho": True, "Default": "A"}, "SuperSecret", Parameter.NO_ECHO_WITH_VALUE),
        ({"Type": "String", "NoEcho": True}, "SuperSecret", Parameter.NO_ECHO_WITH_VALUE),
        ({"Type": "String", "NoEcho": False, "Default": "A"}, "B", "B"),
        ({"Type": "String", "NoEcho": False}, "B", "B"),
        ({"Type": "String", "Default": "abc"}, "B", "B"),
        ({"Type": "String", "Default": None}, None, None),
        ({"Type": "Number", "Default": 1}, None, "1"),
        ({"Type": "List<Number>", "Default": "1,2,3"}, "4,5,6", ["4", "5", "6"]),
        ({"Type": "CommaDelimitedList", "Default": "a,b,c"}, "b,c,d", ["b", "c", "d"]),
    ],
)
def test_get_ref_value(param, provided_value, expected):
    parameter = Parameter(**param)
    assert parameter.get_ref_value(provided_value) == expected
