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

from pycfmodel.model.regexs import CONTAINS_CF_PARAM


class IntrinsicFunctionResolver(object):
    def __init__(self, params, mappings):
        self.params = params
        self.mappings = mappings

    def default_value(self):
        logging.warning("Using default value")
        return "NOVALUE"

    def resolve(self, function):
        if not isinstance(function, dict):
            return function

        (function, function_body), = function.items()

        if function in ["Ref", "Fn::ImportValue"]:
            return self.params.get(self.resolve(function_body), self.default_value())

        elif function == "Fn::Join":
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

        elif function == "Fn::FindInMap":
            map_name, top_level_key, second_level_key = function_body
            map_name = self.resolve(map_name)
            top_level_key = self.resolve(top_level_key)
            second_level_key = self.resolve(second_level_key)
            return self.mappings.get(map_name, {}).get(top_level_key, {}).get(second_level_key, self.default_value())

        elif function == "Fn::Sub":
            replacements = self.params
            if type(function_body) is list:
                text, custom_replacements = function_body
                replacements.update(custom_replacements)
            else:
                text = function_body
            for match in CONTAINS_CF_PARAM.findall(text):
                match_param = match[2:-1]  # Remove ${ and trailing }
                value = self.default_value()
                if match_param in replacements:
                    new_value = self.resolve(replacements[match_param])
                    if isinstance(new_value, str):
                        value = new_value
                text = text.replace(match, value)
            return text

        elif function == "Fn::Select":
            index, list_values = function_body
            return self.resolve(list_values)[int(self.resolve(index))]

        elif function == "Fn::Split":
            delimeter, source_string = function_body
            return self.resolve(source_string).split(self.resolve(delimeter))

        elif function == "Fn::And":
            part_1, part_2 = function_body
            return self.resolve(part_1) and self.resolve(part_2)

        elif function == "Fn::Or":
            part_1, part_2 = function_body
            return self.resolve(part_1) or self.resolve(part_2)

        elif function == "Fn::Not":
            return not self.resolve(function_body[0])

        elif function == "Fn::Equals":
            part_1, part_2 = function_body
            return self.resolve(part_1) == self.resolve(part_2)

        elif function == "Fn::Base64":
            return str(b64encode(self.resolve(function_body).encode("utf-8")), "utf-8")

        # TODO: Implement
        # elif function == "Fn::GetAtt":
        #     return function
        # TODO: Implement condition resolver
        # elif function == "Condition":
        # {"Condition": "SomeOtherCondition"}
        # TODO:Conditions aren't supported yet, so this code can't be evaluated
        # elif function == "Fn::If":
        #     condition, true_section, false_section = function_body
        #     if self.resolve(condition):
        #         return self.resolve(true_section)
        #     else:
        #         return self.resolve(false_section)

        return function
