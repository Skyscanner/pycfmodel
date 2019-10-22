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

from pycfmodel.constants import CONTAINS_STAR, CONTAINS_CF_PARAM


@pytest.mark.parametrize(
    "string, expected",
    [
        ("*", True),
        ("*abc", True),
        ("abc*", True),
        ("abc*def", True),
        ("abc*def*ghi", True),
        ("*abc*def*ghi*", True),
        ("abcdef", False),
    ],
)
def test_contains_star(string, expected):
    assert bool(CONTAINS_STAR.match(string)) == expected


@pytest.mark.parametrize(
    "string, expected",
    [
        ("abcdef", []),
        ("abc${param}def", ["${param}"]),
        ("abc${Ref::abc}def", ["${Ref::abc}"]),
        ("abc${Ref::abc123}def", ["${Ref::abc123}"]),
    ],
)
def test_contains_cf_param(string, expected):
    assert CONTAINS_CF_PARAM.findall(string) == expected
