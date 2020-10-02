from fnmatch import fnmatchcase
from typing import List, Union

from pycfmodel.actions.query import get_all_actions


def _expand_action(action_pattern: str) -> List[str]:
    if isinstance(action_pattern, str):
        action_pattern = action_pattern.lower()
        return sorted(set(action for action in get_all_actions() if fnmatchcase(action.lower(), action_pattern)))

    raise ValueError(f"Not supported type: {type(action_pattern)}")


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
