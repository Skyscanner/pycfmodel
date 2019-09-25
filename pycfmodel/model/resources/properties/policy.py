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
from typing import Dict

from .policy_document import PolicyDocument


class Policy:
    def __init__(self, value: Dict):
        """
        "PolicyDocument" : JSON object,
        "PolicyName" : String,
        """
        self.policy_name = value.get("PolicyName")
        self.policy_document = PolicyDocument(value.get("PolicyDocument"))
