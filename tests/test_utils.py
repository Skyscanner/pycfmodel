from pycfmodel.constants import IMPLEMENTED_FUNCTIONS
from pycfmodel.resolver import FUNCTION_MAPPINGS


def test_implemented_functions():
    assert set(FUNCTION_MAPPINGS) == IMPLEMENTED_FUNCTIONS
