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
from .policy_document import PolicyDocument


class Policy(object):

    def __init__(self, value):
        """
        "PolicyDocument" : JSON object,
        "PolicyName" : String,
        """
        self.policy_name = value.get("PolicyName")
        self.policy_document = PolicyDocument(value.get('PolicyDocument'))

    def resolve(self, intrinsic_function_resolver):
        self.policy_document.resolve(intrinsic_function_resolver)
