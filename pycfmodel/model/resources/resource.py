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

from .properties.policy import Policy


class Resource(object):

    # metadata = None
    _first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    _all_cap_re = re.compile('([a-z0-9])([A-Z])')

    def __init__(self, logical_id, value):
        self.logical_id = logical_id
        self.resource_type = value.get("Type")
        self.metadata = {}

    def set_generic_keys(self, properties, exclude_list):
        generic_keys = set(properties.keys()) - set(exclude_list)
        for generic_key in generic_keys:
            self.__setattr__(
                self._convert_to_snake_case(generic_key),
                properties[generic_key],
            )

    def set_metadata(self, metadata):
        self.metadata = metadata

    def get_policies(self, policies):
        if not policies:
            return []

        new_policies = []
        for p in policies:

            # TODO: a generic function to get if conditions and apply something
            if "Fn::If" in p:
                if_policies = p["Fn::If"]
                new_policies.append(Policy(if_policies[1]))
                new_policies.append(Policy(if_policies[2]))
            else:
                new_policies.append(Policy(p))
        return new_policies

    def get_managed_policy_arns(self, arns):
        if not arns:
            return []

        # TODO: a generic function to get if conditions and apply something
        if isinstance(arns, dict) and "Fn::If" in arns:
            return arns["Fn::If"][1] + arns["Fn::If"][2]
        elif isinstance(arns, list):
            return arns

        return []

    def _convert_to_snake_case(self, name):
        s1 = self._first_cap_re.sub(r'\1_\2', name)
        return self._all_cap_re.sub(r'\1_\2', s1).lower()

    def has_hardcoded_credentials(self):
        if not self.metadata or not self.metadata.get("AWS::CloudFormation::Authentication"):
            return False

        for auth_name, auth in self.metadata.get("AWS::CloudFormation::Authentication", {}).items():
            if auth.get("accessKeyId") or auth.get("password") or auth.get("secretKey"):
                return True
