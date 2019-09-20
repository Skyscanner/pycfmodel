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

from deprecation import deprecated

from pycfmodel.model.regexs import CONTAINS_STAR
from .principal import PrincipalFactory


class Statement(object):

    def __init__(self, statement):
        self.effect_raw = statement.get("Effect")
        self.effect = self.effect_raw

        # TODO: Process condition
        self.condition = statement.get("Condition")

        self.principal = self.__parse_principals(statement.get("Principal"))
        self.not_principal = self.__parse_principals(statement.get("NotPrincipal"))

        self.action_raw = statement.get("Action", [])
        self.action = self.action_raw
        self.not_action_raw = statement.get("NotAction", [])
        self.not_action = self.not_action_raw

        self.resource_raw = statement.get("Resource", [])
        self.resource = self.resource_raw
        self.not_resource_raw = statement.get("NotResource", [])
        self.not_resource = self.not_resource_raw

    def __parse_principals(self, principals):
        principals_factory = PrincipalFactory()
        return principals_factory.generate_principals(principals)

    def actions_with(self, pattern):
        return [action for action in self.get_action_list() if pattern.match(action)]

    def principals_with(self, pattern):
        all = []
        if self.principal:
            all.extend(self.principal)
        if self.not_principal:
            all.extend(self.not_principal)
        return [principal for principal in all if principal.has_principals_with(pattern)]

    @deprecated(deprecated_in="0.4.0", details="Deprecated param pattern. For custom pattern see actions_with")
    def wildcard_actions(self, pattern=None):
        if pattern:
            return self.actions_with(re.compile(pattern))
        return self.actions_with(CONTAINS_STAR)

    @deprecated(deprecated_in="0.4.0", details="Deprecated param pattern. For custom pattern see principals_with")
    def wildcard_principals(self, pattern=None):
        # TODO: change when all classes have implemented resolve
        # all = []
        # if self.principal:
        #     all.extend(self.principal)
        # if self.not_principal:
        #     all.extend(self.not_principal)
        all = []
        if self.principal and isinstance(self.principal, list):
            all.extend(self.principal)
        elif self.principal:
            all.append(self.principal)
        if self.not_principal and isinstance(self.not_principal, list):
            all.extend(self.not_principal)
        elif self.not_principal:
            all.append(self.not_principal)
        if pattern:
            return [principal for principal in all if principal.has_principals_with(re.compile(pattern))]
        return [principal for principal in all if principal.has_wildcard_principals(CONTAINS_STAR)]

    def non_whitelisted_principals(self, whitelist):
        all = []
        if self.principal:
            all.extend(self.principal)
        if self.not_principal:
            all.extend(self.not_principal)
        return [principal for principal in all if principal.has_non_whitelisted_principals(whitelist)]

    def get_action_list(self):
        # TODO: change to return self.action + self.not_action when all classes have implemented resolve
        all = []
        if self.action and isinstance(self.action, list):
            all.extend(self.action)
        elif self.action:
            all.append(self.action)
        if self.not_action and isinstance(self.not_action, list):
            all.extend(self.not_action)
        elif self.not_action:
            all.append(self.not_action)
        return all

    def resolve(self, intrinsic_function_resolver):
        # Effect
        self.effect = intrinsic_function_resolver.resolve(self.effect_raw)

        # Principal
        for principal in self.principal:
            principal.resolve(intrinsic_function_resolver)

        # NotPrincipal
        for principal in self.not_principal:
            principal.resolve(intrinsic_function_resolver)

        # Action
        to_process = self.action_raw
        if not isinstance(to_process, list):
            to_process = [to_process]
        self.action = []
        for identifier in to_process:
            self.action.append(intrinsic_function_resolver.resolve(identifier))

        # NotAction
        to_process = self.not_action_raw
        if not isinstance(to_process, list):
            to_process = [to_process]
        self.not_action = []
        for identifier in to_process:
            self.not_action.append(intrinsic_function_resolver.resolve(identifier))

        # Resource
        to_process = self.resource_raw
        if not isinstance(to_process, list):
            to_process = [to_process]
        self.resource = []
        for identifier in to_process:
            self.resource.append(intrinsic_function_resolver.resolve(identifier))

        # NotResource
        to_process = self.not_resource_raw
        if not isinstance(to_process, list):
            to_process = [to_process]
        self.not_resource = []
        for identifier in to_process:
            self.not_resource.append(intrinsic_function_resolver.resolve(identifier))
