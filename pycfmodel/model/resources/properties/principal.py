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
from pycfmodel.model.regexs import CONTAINS_STAR


class Principal(object):

    def __init__(self, identifier):
        self.identifiers_raw = identifier
        self.identifiers = self.identifiers_raw

    def has_wildcard_identifiers(self):
        return self.has_identifiers_with(CONTAINS_STAR)

    def has_non_whitelisted_identifiers(self, whitelist):
        for type, lst in self.identifiers.items():
            for identifier in lst:
                if identifier not in whitelist:
                    return True
        return False

    def has_identifiers_with(self, pattern):
        for type, lst in self.identifiers.items():
            for identifier in lst:
                if pattern.match(identifier):
                    return True
        return False

    def resolve(self, intrinsic_function_resolver):
        self.identifiers = {}
        for type, lst in self.identifiers_raw.items():
            self.identifiers[type] = []
            if not isinstance(lst, list):
                lst = [lst]
            for identifier in lst:
                self.identifiers[type].append(intrinsic_function_resolver.resolve(identifier))
