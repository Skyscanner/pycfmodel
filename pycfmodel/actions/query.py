from functools import lru_cache
from typing import Dict, Set

from pycfmodel.actions import iam_definition_data


def _get_actions_from_service_info(service_info: Dict) -> Set[str]:
    actions = set()
    service_prefix = service_info["prefix"]
    for privilege in service_info["privileges"].keys():
        actions.add(f"{service_prefix}:{privilege}")
    return actions


@lru_cache(maxsize=None)
def get_all_actions() -> Set[str]:
    actions = set()
    for service_info in iam_definition_data.values():
        actions.update(_get_actions_from_service_info(service_info))
    return actions


@lru_cache(maxsize=None)
def get_actions_for_service(service_prefix) -> Set[str]:
    return _get_actions_from_service_info(iam_definition_data[service_prefix])
