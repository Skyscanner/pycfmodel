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
