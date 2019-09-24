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

from typing import List
from deprecation import deprecated

from pycfmodel.model.regexs import CONTAINS_STAR


class Principal:
    def __init__(self, principal_type, principals):
        self._type = principal_type
        self.principals_raw = principals
        if not isinstance(self.principals_raw, list):
            self.principals_raw = [self.principals_raw]
        self.principals = self.principals_raw

    @deprecated(deprecated_in="0.4.0", details="Deprecated param pattern. For custom pattern see has_principals_with")
    def has_wildcard_principals(self, pattern=None):
        if pattern:
            return self.has_principals_with(re.compile(pattern))
        return self.has_principals_with(CONTAINS_STAR)

    @deprecated(deprecated_in="0.4.0", details="Use has_non_whitelisted_principals")
    def has_nonwhitelisted_principals(self, whitelist):
        return self.has_non_whitelisted_principals(whitelist)

    def has_non_whitelisted_principals(self, whitelist) -> bool:
        for principal in self.principals:
            if principal not in whitelist:
                return True
        return False

    def has_principals_with(self, pattern) -> bool:
        for principal in self.principals:
            if pattern.match(principal):
                return True
        return False

    def resolve(self, intrinsic_function_resolver):
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
