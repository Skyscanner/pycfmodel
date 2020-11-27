import re

import pytest

from pycfmodel.constants import IMPLEMENTED_FUNCTIONS
from pycfmodel.resolver import FUNCTION_MAPPINGS
from pycfmodel.utils import is_conditional_dict, regex_from_cf_string


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


@pytest.mark.parametrize(
    "action, expected_pattern",
    [
        ("", re.compile("^$", re.IGNORECASE)),
        ("*", re.compile("^.*$", re.IGNORECASE)),
        ("?", re.compile("^.{1}$", re.IGNORECASE)),
        ("a", re.compile("^a$", re.IGNORECASE)),
        ("a*", re.compile("^a.*$", re.IGNORECASE)),
        ("a?", re.compile("^a.{1}$", re.IGNORECASE)),
        ("a*a?", re.compile("^a.*a.{1}$", re.IGNORECASE)),
    ],
)
def test_build_regex(action, expected_pattern):
    assert regex_from_cf_string(action) == expected_pattern
