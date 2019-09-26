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
from typing import List, Pattern

from pycfmodel.model.intrinsic_function_resolver import IntrinsicFunctionResolver


class Principal:
    def __init__(self, principal_type, principals):
        self.principal_type = principal_type
        self.principals_raw = principals
        if not isinstance(self.principals_raw, list):
            self.principals_raw = [self.principals_raw]
        self.principals = self.principals_raw

    def has_non_whitelisted_principals(self, whitelist: List[str]) -> bool:
        for principal in self.principals:
            if principal not in whitelist:
                return True
        return False

    def has_principals_with(self, pattern: Pattern) -> bool:
        for principal in self.principals:
            if pattern.match(principal):
                return True
        return False

    def resolve(self, intrinsic_function_resolver: IntrinsicFunctionResolver):
        self.principals = []
        for arn in self.principals_raw:
            self.principals.append(intrinsic_function_resolver.resolve(arn))

    @staticmethod
    def generate_principals(principal_dict) -> List["Principal"]:
        if not principal_dict:
            return []

        if isinstance(principal_dict, str):
            return [Principal(principal_dict, principal_dict)]

        principal_list = []
        for _type, principals in principal_dict.items():
            principal_list.append(Principal(_type, principals))

        return principal_list
