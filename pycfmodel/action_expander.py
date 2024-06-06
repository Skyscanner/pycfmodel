from typing import List, Union

from pycfmodel.cloudformation_actions import CLOUDFORMATION_ACTIONS
from pycfmodel.utils import regex_from_cf_string


def _expand_action(action: str, not_action=False) -> List[str]:
    if isinstance(action, str):
        pattern = regex_from_cf_string(action)
        if not_action:
            return sorted(
                set(CLOUDFORMATION_ACTIONS) - set(action for action in CLOUDFORMATION_ACTIONS if pattern.match(action))
            )
        return sorted(set(action for action in CLOUDFORMATION_ACTIONS if pattern.match(action)))

    raise ValueError(f"Not supported type: {type(action)}")


def _expand_actions(actions: Union[str, List[str]], not_action=False) -> List[str]:
    if isinstance(actions, str):
        return _expand_action(actions, not_action=not_action)

    if isinstance(actions, list):
        expanded_actions = set()
        for action in actions:
            expanded_actions.update(_expand_action(action))
        if not_action:
            return sorted(set(CLOUDFORMATION_ACTIONS) - expanded_actions)
        return sorted(expanded_actions)

    raise ValueError(f"Not supported type: {type(actions)}")


def expand_actions(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if value is None:
                continue  # or obj[key] = None
            elif key == "Action":
                obj[key] = _expand_actions(value)
            elif key == "NotAction":
                obj[key] = _expand_actions(value, not_action=True)
            else:
                obj[key] = expand_actions(value)

    if isinstance(obj, list):
        obj = [expand_actions(value) for value in obj]

    return obj
