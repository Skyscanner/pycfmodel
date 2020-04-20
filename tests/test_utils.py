from typing import Any, List

import pytest

from pycfmodel.constants import IMPLEMENTED_FUNCTIONS
from pycfmodel.resolver import FUNCTION_MAPPINGS
from pycfmodel.utils import convert_to_list


def test_implemented_functions():
    assert set(FUNCTION_MAPPINGS) == IMPLEMENTED_FUNCTIONS


@pytest.mark.parametrize("param, expected_output", [(1, [1]), ([1], [1]), ("a", ["a"]), (["a"], ["a"])])
def test_convert_to_list(param: Any, expected_output: List):
    assert convert_to_list(param) == expected_output
