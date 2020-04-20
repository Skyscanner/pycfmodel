from typing import Any, List, Union

from pycfmodel.constants import IMPLEMENTED_FUNCTIONS


def is_resolvable_dict(value: Any) -> bool:
    return isinstance(value, dict) and len(value) == 1 and next(iter(value)) in IMPLEMENTED_FUNCTIONS


def convert_to_list(item: Union[Any, List[Any]]) -> List[Any]:
    if isinstance(item, list):
        return item
    return [item]
