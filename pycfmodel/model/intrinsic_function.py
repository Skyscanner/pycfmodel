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
from datetime import date
from typing import Dict, List, Union

from pycfmodel.model.regexs import CONTAINS_CF_PARAM

logger = logging.getLogger(__file__)

ValidResolvers = Union[str, int, bool, float, List, Dict, date]


def resolve(input: ValidResolvers, params: Dict, mappings: Dict[str, Dict]):
    if input is None or isinstance(input, (str, int, bool, float, date)):
        return input

    elif isinstance(input, list):
        return [resolve(entry, params, mappings) for entry in input]

    elif isinstance(input, dict):
        function_name = next(iter(input.keys()))
        if len(input) == 1 and function_name in FUNCTION_MAPPINGS:
            function_resolver = FUNCTION_MAPPINGS[function_name]
            return function_resolver(input[function_name], params, mappings)

        return {k: resolve(v, params, mappings) for k, v in input.items()}


def resolve_ref(function_body, params: Dict, mappings: Dict[str, Dict]):
    resolved_ref = resolve(function_body, params, mappings)
    if resolved_ref in params:
        return params[resolved_ref]
    else:
        logger.warning(f"Using default value for param {function_body}")
        return "UNDEFINED_PARAM"


def resolve_join(function_body, params: Dict, mappings: Dict[str, Dict]):
    delimiter, list_values = function_body
    resolved_delimiter = resolve(delimiter, params, mappings)
    resolved_list = resolve(list_values, params, mappings)
    return resolved_delimiter.join(resolved_list)


def resolve_find_in_map(function_body, params: Dict, mappings: Dict[str, Dict]):
    map_name, top_level_key, second_level_key = function_body
    map_name = resolve(map_name, params, mappings)
    top_level_key = resolve(top_level_key, params, mappings)
    second_level_key = resolve(second_level_key, params, mappings)

    resolved_mapping = mappings.get(map_name, {}).get(top_level_key, {}).get(second_level_key)
    if resolved_mapping:
        return resolved_mapping
    else:
        logger.warning(f"Using default value for mapping {[map_name, top_level_key, second_level_key]}")
        return "UNDEFINED_MAPPING"


def resolve_sub(function_body, params: Dict, mappings: Dict[str, Dict]):
    replacements = params
    # Whenever we receive a list, first parameter is a text and the second one is a dict with custom replacements.
    # Whenever we receive a list, we need to resolve inlined variables
    if isinstance(function_body, list):
        text, custom_replacements = function_body
        replacements.update(custom_replacements)
    else:
        text = function_body

    for match in CONTAINS_CF_PARAM.findall(text):
        match_param = match[2:-1]  # Remove ${ and trailing }
        if match_param in replacements:
            value = resolve(replacements[match_param], params, mappings)
            text = text.replace(match, value)
    return text


def resolve_select(function_body, params: Dict, mappings: Dict[str, Dict]):
    index, list_values = function_body
    resolved_index = int(resolve(index, params, mappings))
    resolved_list = resolve(list_values, params, mappings)
    return resolved_list[resolved_index]


def resolve_split(function_body, params: Dict, mappings: Dict[str, Dict]):
    delimiter, source_string = function_body
    resolved_delimiter = resolve(delimiter, params, mappings)
    resolved_source_string = resolve(source_string, params, mappings)
    return resolved_source_string.split(resolved_delimiter)


def resolve_if(function_body, params: Dict, mappings: Dict[str, Dict]):
    # TODO: Uncomment when Conditions are ready
    # condition, true_section, false_section = function_body
    # if resolve(condition, params, mappings):
    #     return resolve(true_section, params, mappings)
    # else:
    #     return resolve(false_section, params, mappings)
    logger.warning(f"`Fn::If` resolver not implemented, returning if body")
    return function_body


def resolve_and(function_body: List, params: Dict, mappings: Dict[str, Dict]):
    part_1, part_2 = function_body
    return resolve(part_1, params, mappings) and resolve(part_2, params, mappings)


def resolve_or(function_body: List, params: Dict, mappings: Dict[str, Dict]):
    part_1, part_2 = function_body
    return resolve(part_1, params, mappings) or resolve(part_2, params, mappings)


def resolve_not(function_body: List, params: Dict, mappings: Dict[str, Dict]):
    return not resolve(function_body[0], params, mappings)


def resolve_equals(function_body: List, params: Dict, mappings: Dict[str, Dict]):
    part_1, part_2 = function_body
    return resolve(part_1, params, mappings) == resolve(part_2, params, mappings)


def resolve_base64(function_body: str, params: Dict, mappings: Dict[str, Dict]):
    resolved_string = resolve(function_body, params, mappings)
    return str(b64encode(resolved_string.encode("utf-8")), "utf-8")


def resolve_get_attr(function_body, params: Dict, mappings: Dict[str, Dict]):
    # TODO: Implement. Conditions aren't supported yet, so this code can't be evaluated
    logger.warning(f"`Fn::GetAtt` resolver not implemented, returning getattr body")
    return function_body


def resolve_condition(function_body, params: Dict, mappings: Dict[str, Dict]):
    # {"Condition": "SomeOtherCondition"}
    # TODO: Implement. Conditions aren't supported yet, so this code can't be evaluated
    logger.warning(f"`Condition` resolver not implemented, returning condition body")
    return function_body


FUNCTION_MAPPINGS = {
    "Ref": resolve_ref,
    "Fn::ImportValue": resolve_ref,
    "Fn::Join": resolve_join,
    "Fn::FindInMap": resolve_find_in_map,
    "Fn::Sub": resolve_sub,
    "Fn::Select": resolve_select,
    "Fn::Split": resolve_split,
    "Fn::If": resolve_if,
    "Fn::And": resolve_and,
    "Fn::Or": resolve_or,
    "Fn::Not": resolve_not,
    "Fn::Equals": resolve_equals,
    "Fn::Base64": resolve_base64,
    "Fn::GetAtt": resolve_get_attr,
    "Condition": resolve_condition,
}
