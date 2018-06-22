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


class IAMManagedPolicy(Resource):

    def __init__(self, logical_id, value):
        """
        "Description" : String,
        "Groups" : [ String, ... ],
        "Path" : String,
        "PolicyDocument" : JSON object,
        "Roles" : [ String, ... ],
        "Users" : [ String, ... ],
        "ManagedPolicyName" : String
        """
        super().__init__(logical_id, value)

        self.description = None
        self.groups = []
        self.path = None
        self.roles = []
        self.users = []
        self.managed_policy_name = None

        self.policy_document = PolicyDocument(
            value.get("Properties", {}).get('PolicyDocument')
        )
        self.set_generic_keys(value.get("Properties", {}), ["PolicyDocument"])
