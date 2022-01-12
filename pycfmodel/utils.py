import re
from ipaddress import IPv4Network, IPv6Network
from typing import Any, List, Pattern, Union

from pycfmodel.constants import IMPLEMENTED_FUNCTIONS


def is_resolvable_dict(value: Any) -> bool:
    return isinstance(value, dict) and len(value) == 1 and next(iter(value)) in IMPLEMENTED_FUNCTIONS


def convert_to_list(item: Union[Any, List[Any]]) -> List[Any]:
    if isinstance(item, list):
        return item
    return [item]


def regex_from_cf_string(action: str) -> Pattern:
    # Replace *
    action = action.replace("*", ".*")

    # Replace ?
    action = action.replace("?", ".{1}")

    return re.compile(f"^{action}$", re.IGNORECASE)


def not_ip(arg: Any) -> bool:
    return not isinstance(arg, IPv4Network) and not isinstance(arg, IPv6Network)
