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
from typing import List, Collection


class Principal:
    def __init__(self, principal_type, principals):
        self.principal_type = principal_type
        self.principals = self._parse_principals(principals)

    def _parse_principals(self, principals) -> List[str]:
        if isinstance(principals, str):
            return [principals]

        if isinstance(principals, list):
            return principals

        # TODO: unhandled cases
        return []

    def has_wildcard_principals(self, pattern=None) -> bool:
        for principal in self.principals:
            if pattern and isinstance(principal, str) and re.match(pattern, principal):
                return True
            elif principal == "*":
                return True
        return False

    def has_nonwhitelisted_principals(self, whitelist: Collection) -> bool:
        for principal in self.principals:
            if principal not in whitelist:
                return True
        return False

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
