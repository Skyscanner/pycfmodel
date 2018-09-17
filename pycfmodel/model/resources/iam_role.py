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
from .resource import Resource
from .properties.policy_document import PolicyDocument


class IAMRole(Resource):

    def __init__(self, logical_id, value):
        """
        "AssumeRolePolicyDocument": { JSON },
        "ManagedPolicyArns": [ String, ... ],
        "Path": String,
        "Policies": [ Policies, ... ],
        "RoleName": String
        """
        super().__init__(logical_id, value)

        self.path = None
        self.policies = []
        self.role_name = None

        self.assume_role_policy_document = PolicyDocument(
            value.get("Properties", {}).get("AssumeRolePolicyDocument"),
        )
        self.policies = self.get_policies(
            value.get("Properties", {}).get("Policies"),
        )
        self.managed_policy_arns = self.get_managed_policy_arns(
            value.get("Properties", {}).get("ManagedPolicyArns"),
        )
        self.set_generic_keys(
            value.get("Properties", {}),
            ["AssumeRolePolicyDocument", "Policies", "ManagedPolicyArns"],
        )
