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
from typing import List, Pattern

from deprecation import deprecated

from pycfmodel.model.intrinsic_function_resolver import IntrinsicFunctionResolver
from pycfmodel.model.regexs import CONTAINS_STAR
from .principal import Principal


class Statement:
    def __init__(self, statement):
        self.effect_raw = statement.get("Effect")
        self.effect = self.effect_raw

        # TODO: Process condition
        self.condition = statement.get("Condition", {})

        self.principal = Principal.generate_principals(statement.get("Principal"))
        self.not_principal = Principal.generate_principals(statement.get("NotPrincipal"))

        self.action_raw = statement.get("Action", [])
        if not isinstance(self.action_raw, list):
            self.action_raw = [self.action_raw]
        self.action = self.action_raw

        self.not_action_raw = statement.get("NotAction", [])
        if not isinstance(self.not_action_raw, list):
            self.not_action_raw = [self.not_action_raw]
        self.not_action = self.not_action_raw

        self.resource_raw = statement.get("Resource", [])
        if not isinstance(self.resource_raw, list):
            self.resource_raw = [self.resource_raw]
        self.resource = self.resource_raw

        self.not_resource_raw = statement.get("NotResource", [])
        if not isinstance(self.not_resource_raw, list):
            self.not_resource_raw = [self.not_resource_raw]
        self.not_resource = self.not_resource_raw

    def actions_with(self, pattern: Pattern) -> List[str]:
        return [action for action in self.get_action_list() if pattern.match(action)]

    def principals_with(self, pattern) -> List[Principal]:
        all = self.principal + self.not_principal
        return [principal for principal in all if principal.has_principals_with(pattern)]

    @deprecated(deprecated_in="0.4.0", details="Deprecated param pattern. For custom pattern see actions_with")
    def wildcard_actions(self, pattern=None) -> List[str]:
        if pattern:
            return self.actions_with(re.compile(pattern))
        return self.actions_with(CONTAINS_STAR)

    @deprecated(deprecated_in="0.4.0", details="Deprecated param pattern. For custom pattern see principals_with")
    def wildcard_principals(self, pattern: str) -> List[Principal]:
        all = self.principal + self.not_principal
        if pattern:
            return [principal for principal in all if principal.has_principals_with(re.compile(pattern))]
        return [principal for principal in all if principal.has_wildcard_principals(CONTAINS_STAR)]

    def non_whitelisted_principals(self, whitelist: List[str]) -> List[Principal]:
        all = self.principal + self.not_principal
        return [principal for principal in all if principal.has_non_whitelisted_principals(whitelist)]

    def get_action_list(self) -> List[str]:
        return self.action + self.not_action

    def resolve(self, intrinsic_function_resolver: IntrinsicFunctionResolver):
        # Effect
        self.effect = intrinsic_function_resolver.resolve(self.effect_raw)

        # Principal
        for principal in self.principal:
            principal.resolve(intrinsic_function_resolver)

        # NotPrincipal
        for principal in self.not_principal:
            principal.resolve(intrinsic_function_resolver)

        # Action
        self.action = []
        for identifier in self.action_raw:
            self.action.append(intrinsic_function_resolver.resolve(identifier))

        # NotAction
        self.not_action = []
        for identifier in self.not_action_raw:
            self.not_action.append(intrinsic_function_resolver.resolve(identifier))

        # Resource
        self.resource = []
        for identifier in self.resource_raw:
            self.resource.append(intrinsic_function_resolver.resolve(identifier))

        # NotResource
        self.not_resource = []
        for identifier in self.not_resource_raw:
            self.not_resource.append(intrinsic_function_resolver.resolve(identifier))
