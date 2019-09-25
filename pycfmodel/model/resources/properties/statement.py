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

import re
from typing import List

from .principal import Principal


class Statement:
    def __init__(self, statement):
        self.action = statement.get("Action", [])
        self.resource = statement.get("Resource", [])
        self.principal = Principal.generate_principals(statement.get("Principal"))
        self.effect = statement.get("Effect")
        self.condition = statement.get("Condition", {})
        self.not_action = statement.get("NotAction", {})
        self.not_principal = statement.get("NotPrincipal", {})
        if not isinstance(self.action, list):
            self.action = [self.action]
        if not isinstance(self.resource, list):
            self.resource = [self.resource]

    def wildcard_actions(self, pattern=None) -> List[str]:
        if not self.action:
            return []

        if pattern:
            return [a for a in self.action if re.match(pattern, a)]

        return [a for a in self.action if "*" in str(a)]

    def wildcard_principals(self, pattern: str) -> List[Principal]:
        if not self.principal:
            return []

        wildcard_principals = []
        for principal in self.principal:
            if principal.has_wildcard_principals(pattern):
                wildcard_principals.append(principal)

        return wildcard_principals

    def non_whitelisted_principals(self, whitelist: List[str]) -> List[Principal]:
        if not self.principal or self.condition:
            return []

        nonwhitelisted_principals = []
        for principal in self.principal:
            if principal.has_nonwhitelisted_principals(whitelist):
                nonwhitelisted_principals.append(principal)

        return nonwhitelisted_principals

    def get_action_list(self) -> List[str]:
        if isinstance(self.action, str):
            return [self.action]
        elif isinstance(self.action, list):
            return self.action
        return []
