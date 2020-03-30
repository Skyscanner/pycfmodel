from typing import Any

from pycfmodel.constants import CONDITION_FUNCTIONS, IMPLEMENTED_FUNCTIONS


def is_resolvable_dict(value: Any) -> bool:
    return isinstance(value, dict) and len(value) == 1 and next(iter(value)) in IMPLEMENTED_FUNCTIONS


def is_conditional_dict(value: Any) -> bool:
    if isinstance(value, dict):
        for func in value.keys():
            if not any(f in func for f in CONDITION_FUNCTIONS):
                return False
        return True
    return False
