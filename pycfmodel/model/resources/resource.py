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
from typing import Dict, List

import inflection

from .properties.policy import Policy


class Resource:
    def __init__(self, logical_id, value):
        self.logical_id = logical_id
        self.resource_type = value.get("Type")
        self.properties = {}
        self.metadata = value.get("Metadata", {})
        self.set_generic_keys(value.get("Properties", {}), [])

    def set_generic_keys(self, properties: Dict, exclude_list: List):
        generic_keys = set(properties.keys()) - set(exclude_list)
        for generic_key in generic_keys:
            self.__setattr__(inflection.underscore(generic_key), properties[generic_key])

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

    def has_hardcoded_credentials(self):
        if self.resource_type == "AWS::IAM::User" and self.properties:
            login_profile = self.properties.get("LoginProfile", {})
            if "Password" in list(login_profile):
                return True

        if not self.metadata or not self.metadata.get("AWS::CloudFormation::Authentication"):
            return False

        for auth_name, auth in self.metadata.get("AWS::CloudFormation::Authentication", {}).items():
            if auth.get("accessKeyId") or auth.get("password") or auth.get("secretKey"):
                return True
