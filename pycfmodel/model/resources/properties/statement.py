"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import logging

from typing import List, Pattern, Optional, Union, Dict

from ....utils import is_resolvable_dict
from ...types import ResolvableStr, ResolvableStrOrList
from .property import Property

logger = logging.getLogger(__file__)

PrincipalTypes = Union[ResolvableStr, List[ResolvableStr], Dict[str, Union[ResolvableStr, List[ResolvableStr]]]]


class Statement(Property):
    Sid: Optional[ResolvableStr] = None
    Effect: Optional[ResolvableStr] = None
    Principal: Optional[PrincipalTypes] = None
    NotPrincipal: Optional[PrincipalTypes] = None
    Action: Optional[ResolvableStrOrList] = None
    NotAction: Optional[ResolvableStrOrList] = None
    Resource: Optional[ResolvableStrOrList] = None
    NotResource: Optional[ResolvableStrOrList] = None

    def get_action_list(self) -> List[ResolvableStr]:
        action_list = []
        for actions in [self.Action, self.NotAction]:
            if isinstance(actions, List):
                action_list.extend(actions)
            elif isinstance(actions, (str, dict)):
                action_list.append(actions)
        return action_list

    def get_resource_list(self) -> List[ResolvableStr]:
        resource_list = []
        for resources in [self.Resource, self.NotResource]:
            if isinstance(resources, List):
                resource_list.extend(resources)
            elif isinstance(resources, (str, dict)):
                resource_list.append(resources)
        return resource_list

    def get_principal_list(self) -> List[ResolvableStr]:
        principal_list = []
        for principals in [self.Principal, self.NotPrincipal]:
            if isinstance(principals, list):
                principal_list.extend(principals)
            elif isinstance(principals, str):
                principal_list.append(principals)
            elif is_resolvable_dict(principals):
                principal_list.append(principals)
            elif isinstance(principals, dict):
                for value in principals.values():
                    if isinstance(value, (str, Dict)):
                        principal_list.append(value)
                    elif isinstance(value, List):
                        principal_list.extend(value)
            elif principals is not None:
                raise ValueError(f"Not supported type: {type(principals)}")
        return principal_list

    def actions_with(self, pattern: Pattern) -> List[str]:
        return [action for action in self.get_action_list() if isinstance(action, str) and pattern.match(action)]

    def principals_with(self, pattern: Pattern) -> List[str]:
        return [
            principal
            for principal in self.get_principal_list()
            if isinstance(principal, str) and pattern.match(principal)
        ]

    def resources_with(self, pattern: Pattern) -> List[str]:
        return [
            resource for resource in self.get_resource_list() if isinstance(resource, str) and pattern.match(resource)
        ]

    def non_whitelisted_principals(self, whitelist: List[str]) -> List[str]:
        return [
            principal
            for principal in self.get_principal_list()
            if isinstance(principal, str) and principal not in whitelist
        ]
