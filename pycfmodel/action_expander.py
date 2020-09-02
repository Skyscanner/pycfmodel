import re
from typing import List, Pattern, Union

from pycfmodel.cloudformation_actions import CLOUDFORMATION_ACTIONS


def _build_regex(action: str) -> Pattern:
    # Replace *
    action = action.replace("*", ".*")

    # Replace ?
    action = action.replace("?", ".{1}")

    return re.compile(f"^{action}$", re.IGNORECASE)


def _expand_action(action: str) -> List[str]:
    if isinstance(action, str):
        pattern = _build_regex(action)
        return sorted(set(action for action in CLOUDFORMATION_ACTIONS if pattern.match(action)))

    raise ValueError(f"Not supported type: {type(action)}")


def _expand_actions(actions: Union[str, List[str]]) -> List[str]:
    if isinstance(actions, str):
        return _expand_action(actions)

    if isinstance(actions, list):
        expanded_actions = set()
        for action in actions:
            expanded_actions.update(_expand_action(action))
        return sorted(expanded_actions)

    raise ValueError(f"Not supported type: {type(actions)}")


def expand_actions(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ("Action", "NotAction"):
                obj[key] = _expand_actions(value)
            else:
                obj[key] = expand_actions(value)

    if isinstance(obj, list):
        obj = [expand_actions(value) for value in obj]

    return obj
