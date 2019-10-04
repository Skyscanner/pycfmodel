"""
Copyright 2018-2019 Skyscanner Ltd

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

from .property import Property
from ...types import ResolvableStr

logger = logging.getLogger(__file__)

PrincipalTypes = Union[ResolvableStr, List[ResolvableStr], Dict[str, Union[ResolvableStr, List[ResolvableStr]]]]


class Statement(Property):
    Sid: Optional[str] = None
    Effect: Optional[str] = None
    Condition: Optional[str] = None
    Principal: Optional[PrincipalTypes] = None
    NotPrincipal: Optional[PrincipalTypes] = None
    Action: Optional[Union[str, List, Dict]] = None
    NotAction: Optional[Union[str, List, Dict]] = None
    Resource: Optional[Union[str, List, Dict]] = None
    NotResource: Optional[Union[str, List, Dict]] = None

    def get_action_list(self) -> List[ResolvableStr]:
        actions = []

        if isinstance(self.Action, List):
            actions.extend(self.Action)
        elif isinstance(self.Action, (str, dict)):
            actions.append(self.Action)

        if isinstance(self.NotAction, List):
            actions.extend(self.NotAction)
        elif isinstance(self.NotAction, (str, dict)):
            actions.append(self.NotAction)

        return actions

    def get_resource_list(self) -> List[ResolvableStr]:
        resources = []

        if isinstance(self.Resource, List):
            resources.extend(self.Resource)
        elif isinstance(self.Resource, (str, dict)):
            resources.append(self.Resource)

        if isinstance(self.NotResource, List):
            resources.extend(self.NotResource)
        elif isinstance(self.NotResource, (str, dict)):
            resources.append(self.NotResource)

        return resources

    def get_principal_list(self) -> List[ResolvableStr]:
        principals = []

        if isinstance(self.Principal, list):
            principals.extend(self.Principal)
        elif isinstance(self.Principal, str):
            principals.append(self.Principal)
        elif isinstance(self.Principal, dict):
            if len(self.Principal) == 1 and next(iter(self.Principal)).startswith("Fn"):
                principals.append(self.Principal)
            else:
                for value in self.Principal.values():
                    if isinstance(value, (str, Dict)):
                        principals.append(value)
                    elif isinstance(value, List):
                        principals.extend(value)

        if isinstance(self.NotPrincipal, list):
            principals.extend(self.NotPrincipal)
        elif isinstance(self.NotPrincipal, str):
            principals.append(self.NotPrincipal)
        elif isinstance(self.NotPrincipal, dict):
            if len(self.NotPrincipal) == 1 and next(iter(self.NotPrincipal)).startswith("Fn"):
                principals.append(self.NotPrincipal)
            else:
                for value in self.NotPrincipal.values():
                    if isinstance(value, (str, Dict)):
                        principals.append(value)
                    elif isinstance(value, List):
                        principals.extend(value)

        return principals

    def actions_with(self, pattern: Pattern) -> List[str]:
        return [action for action in self.get_action_list() if isinstance(action, str) and pattern.match(action)]

    def principals_with(self, pattern: Pattern) -> List:
        return [
            principal
            for principal in self.get_principal_list()
            if isinstance(principal, str) and pattern.match(principal)
        ]

    def resources_with(self, pattern: Pattern) -> List:
        return [
            resource for resource in self.get_resource_list() if isinstance(resource, str) and pattern.match(resource)
        ]

    def non_whitelisted_principals(self, whitelist: List[str]) -> List:
        return [
            principal
            for principal in self.get_principal_list()
            if isinstance(principal, str) and principal not in whitelist
        ]
