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
import logging

from base64 import b64encode
from typing import Dict

from pycfmodel.model.regexs import CONTAINS_CF_PARAM


class IntrinsicFunctionResolver:
    def __init__(self, params: Dict, mappings: Dict):
        self.params = params
        self.mappings = mappings
        self.functions = {
            "Ref": self._ref,
            "Fn::ImportValue": self._ref,
            "Fn::Join": self._join,
            "Fn::FindInMap": self._find_in_map,
            "Fn::Sub": self._sub,
            "Fn::Select": self._select,
            "Fn::Split": self._split,
            "Fn::If": self._if,
            "Fn::And": self._and,
            "Fn::Or": self._or,
            "Fn::Not": self._not,
            "Fn::Equals": self._equals,
            "Fn::Base64": self._base64,
            "Fn::GetAtt": self._get_attr,
            "Condition": self._condition,
        }

    def default_value(self):
        logging.warning("Using default value")
        return "NOVALUE"

    def resolve(self, function):
        if not isinstance(function, dict):
            return function
        (function, function_body), = function.items()
        func_resolver = self.functions.get(function)
        return func_resolver(function_body) if func_resolver else function

    def _ref(self, function_body):
        return self.params.get(self.resolve(function_body), self.default_value())

    def _join(self, function_body):
        delimiter, values = function_body
        delimiter = self.resolve(delimiter)
        if not isinstance(delimiter, str):
            delimiter = self.default_value()
        result = []
        for value in values:
            resolved_value = self.resolve(value)
            if isinstance(resolved_value, str):
                result.append(resolved_value)
        return delimiter.join(result)

    def _find_in_map(self, function_body):
        map_name, top_level_key, second_level_key = function_body
        map_name = self.resolve(map_name)
        top_level_key = self.resolve(top_level_key)
        second_level_key = self.resolve(second_level_key)
        return self.mappings.get(map_name, {}).get(top_level_key, {}).get(second_level_key, self.default_value())

    def _sub(self, function_body):
        replacements = self.params
        if type(function_body) is list:
            text, custom_replacements = function_body
            replacements.update(custom_replacements)
        else:
            text = function_body
        for match in CONTAINS_CF_PARAM.findall(text):
            match_param = match[2:-1]  # Remove ${ and trailing }
            if match_param in replacements:
                new_value = self.resolve(replacements[match_param])
                if isinstance(new_value, str):
                    value = new_value
                else:
                    value = self.default_value()
                text = text.replace(match, value)
        return text

    def _select(self, function_body):
        index, list_values = function_body
        return self.resolve(list_values)[int(self.resolve(index))]

    def _split(self, function_body):
        delimeter, source_string = function_body
        return self.resolve(source_string).split(self.resolve(delimeter))

    def _if(self, function_body):
        # TODO: Uncomment whne conditionals are ready
        # condition, true_section, false_section = function_body
        # if self.resolve(condition):
        #     return self.resolve(true_section)
        # else:
        #     return self.resolve(false_section)
        return function_body

    def _and(self, function_body):
        part_1, part_2 = function_body
        return self.resolve(part_1) and self.resolve(part_2)

    def _or(self, function_body):
        part_1, part_2 = function_body
        return self.resolve(part_1) or self.resolve(part_2)

    def _not(self, function_body):
        return not self.resolve(function_body[0])

    def _equals(self, function_body):
        part_1, part_2 = function_body
        return self.resolve(part_1) == self.resolve(part_2)

    def _base64(self, function_body):
        return str(b64encode(self.resolve(function_body).encode("utf-8")), "utf-8")

    def _get_attr(self, function_body):
        # TODO: Implement
        return function_body

    def _condition(self, function_body):
        # {"Condition": "SomeOtherCondition"}
        # TODO: Implement. Conditions aren't supported yet, so this code can't be evaluated
        return function_body
