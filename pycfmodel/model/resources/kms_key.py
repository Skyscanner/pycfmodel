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


class KMSKey(Resource):

    def __init__(self, logical_id, value):
        """
        "Description" : String,
        "Enabled" : Boolean,
        "EnableKeyRotation" : Boolean,
        "KeyPolicy" : JSON object,
        "KeyUsage" : String,
        "PendingWindowInDays" : Integer,
        "Tags" : [ Resource Tag, ... ]
        """
        super().__init__(logical_id, value)

        self.description = None
        self.enabled = False
        self.enable_key_rotation = False
        self.key_usage = None
        self.pending_window_in_days = None
        self.tags = []

        self.key_policy = PolicyDocument(
            value.get("Properties", {}).get("KeyPolicy"))

        self.set_generic_keys(value.get("Properties", {}), ["KeyPolicy"])
