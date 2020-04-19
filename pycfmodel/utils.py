from typing import Any

from pycfmodel.constants import IMPLEMENTED_FUNCTIONS


def is_resolvable_dict(value: Any) -> bool:
    return isinstance(value, dict) and len(value) == 1 and next(iter(value)) in IMPLEMENTED_FUNCTIONS
