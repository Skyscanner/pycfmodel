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
from pycfmodel.model.utils import convert_to_snake_case


class Output(object):

    def __init__(self, logical_id, properties, value=None):
        if not isinstance(properties, dict):
            return
        self.logical_id = logical_id
        self.type = properties.get("Type")
        self.default = properties.get("Default")
        if value:
            self.value = value
        else:
            self.value = self.default
        self.description = properties.get("Description")

        self.set_generic_keys(properties, ["Type", "Default", "Description"])

    def set_generic_keys(self, properties, exclude_list):
        """
        Sets all the key value pairs that were not set manually in __init__.
        """

        generic_keys = set(properties.keys()) - set(exclude_list)
        for generic_key in generic_keys:
            self.__setattr__(
                convert_to_snake_case(generic_key),
                properties[generic_key],
            )
