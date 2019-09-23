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
from typing import List

import inflection


class Parameter:
    def __init__(self, logical_id: str, properties):
        if not isinstance(properties, dict):
            return
        self.logical_id = logical_id
        self.type = properties.get("Type")

        self.set_generic_keys(properties, ["Type"])

    def set_generic_keys(self, properties: dict, exclude_list: List[str]):
        """
        Sets all the key value pairs that were not set manually in __init__.
        """

        generic_keys = set(properties.keys()) - set(exclude_list)
        for generic_key in generic_keys:
            self.__setattr__(inflection.underscore(generic_key), properties[generic_key])
