"""
Copyright 2018 Skyscanner Ltd

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

from .principal import PrincipalFactory


class Statement(object):

    def __init__(self, statement):
        self.action = statement.get("Action")
        self.resource = statement.get("Resource")
        self.principal = self.__parse_principals(statement.get("Principal"))
        self.effect = statement.get("Effect")
        self.condition = statement.get("Condition", {})
        self.not_action = statement.get("NotAction", {})
        self.not_principal = statement.get("NotPrincipal", {})

    def __parse_principals(self, principals):
        principals_factory = PrincipalFactory()
        return principals_factory.generate_principals(principals)

    def wildcard_actions(self, pattern=None):
        if not self.action:
            return []

        if not isinstance(self.action, list):
            self.action = [self.action]

        if pattern:
            return [
                a for a in self.action
                if re.match(pattern, a)
            ]

        return [a for a in self.action if "*" in str(a)]

    def wildcard_principals(self, pattern):
        if not self.principal:
            return []

        wildcard_principals = []
        for principal in self.principal:
            if principal.has_wildcard_principals(pattern):
                wildcard_principals.append(principal)

        return wildcard_principals

    def non_whitelisted_principals(self, whitelist):
        if not self.principal or self.condition:
            return []

        nonwhitelisted_principals = []
        for principal in self.principal:
            if principal.has_nonwhitelisted_principals(whitelist):
                nonwhitelisted_principals.append(principal)

        return nonwhitelisted_principals

    def get_action_list(self):
        if isinstance(self.action, str):
            return [self.action]
        elif isinstance(self.action, list):
            return self.action
        return []
