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


class Principal(object):

    def __init__(self, _type, principals):
        self._type = _type
        self.principals = self.parse_principals(principals)

    def parse_principals(self, principals):
        if isinstance(principals, str):
            return [principals]

        if isinstance(principals, list):
            return principals

        # TODO: unhandled cases
        return []

    def has_wildcard_principals(self, pattern=None):
        for principal in self.principals:
            if pattern and isinstance(principal, str) and re.match(pattern, principal):
                return True
            elif principal == "*":
                return True
        return False

    def has_nonwhitelisted_principals(self, whitelist):
        for principal in self.principals:
            if principal not in whitelist:
                return True
        return False


class PrincipalFactory(object):

    @staticmethod
    def generate_principals(principal_dict):
        if not principal_dict:
            return []

        if isinstance(principal_dict, str):
            return [Principal(principal_dict, principal_dict)]

        principal_list = []
        for _type, principals in principal_dict.items():
            principal_list.append(Principal(_type, principals))

        return principal_list
