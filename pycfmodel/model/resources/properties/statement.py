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
from pycfmodel.model.regexs import CONTAINS_STAR
from .principal import Principal


class Statement(object):

    def __init__(self, statement):
        self.effect_raw = statement.get("Effect")
        self.effect = self.effect_raw

        # @TODO Process condition
        self.condition = statement.get("Condition")

        self.principal = None
        self.not_principal = None

        if "Principal" in statement:
            self.principal = Principal(statement.get("Principal"))
        if "NotPrincipal" in statement:
            self.not_principal = Principal(statement.get("NotPrincipal"))

        self.action_raw = statement.get("Action", [])
        self.action = self.action_raw
        self.not_action_raw = statement.get("NotAction", [])
        self.not_action = self.not_action_raw

        self.resource_raw = statement.get("Resource", [])
        self.resource = self.resource_raw
        self.not_resource_raw = statement.get("NotResource", [])
        self.not_resource = self.not_resource_raw

    def has_actions_with(self, pattern):
        all = []
        if self.action:
            all.extend(self.action)
        if self.not_action:
            all.extend(self.not_action)
        return [action for action in all if pattern.match(action)]

    def wildcard_actions(self):
        return self.has_actions_with(CONTAINS_STAR)

    def wildcard_principals(self):
        all = []
        if self.principal:
            all.extend(self.principal)
        if self.not_principal:
            all.extend(self.not_principal)
        return [principal for principal in all if principal.has_wildcard_principals()]

    def non_whitelisted_principals(self, whitelist):
        all = []
        if self.principal:
            all.extend(self.principal)
        if self.not_principal:
            all.extend(self.not_principal)
        return [principal for principal in all if principal.has_non_whitelisted_principals(whitelist)]

    def get_action_list(self):
        all = []
        if self.action:
            all.extend(self.action)
        if self.not_action:
            all.extend(self.not_action)
        return all

    def resolve(self, intrinsic_function_resolver):
        # Effect
        self.effect = intrinsic_function_resolver.resolve(self.effect_raw)

        # Principal
        if self.principal:
            self.principal.resolve(intrinsic_function_resolver)

        # NotPrincipal
        if self.not_principal:
            self.not_principal.resolve(intrinsic_function_resolver)

        # Action
        to_process = []
        if not isinstance(self.action_raw, list):
            to_process = [self.action_raw]
        self.action = []
        for identifier in to_process:
            self.action.append(intrinsic_function_resolver.resolve(identifier))

        # NotAction
        to_process = []
        if not isinstance(self.not_action_raw, list):
            to_process = [self.not_action_raw]
        self.not_action = []
        for identifier in to_process:
            self.not_action.append(intrinsic_function_resolver.resolve(identifier))

        # Resource
        to_process = []
        if not isinstance(self.resource_raw, list):
            to_process = [self.resource_raw]
        self.resource = []
        for identifier in to_process:
            self.resource.append(intrinsic_function_resolver.resolve(identifier))

        # NotResource
        to_process = []
        if not isinstance(self.not_resource_raw, list):
            to_process = [self.not_resource_raw]
        self.not_resource = []
        for identifier in to_process:
            self.not_resource.append(intrinsic_function_resolver.resolve(identifier))
