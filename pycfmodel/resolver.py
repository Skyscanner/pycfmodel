import logging

from base64 import b64encode
from datetime import date
from ipaddress import IPv4Network, IPv6Network
from typing import Dict, List, Union

from pydantic import BaseModel

from pycfmodel.constants import AWS_NOVALUE, CONTAINS_CF_PARAM
from pycfmodel.utils import is_resolvable_dict

logger = logging.getLogger(__file__)

ValidResolvers = Union[str, int, bool, float, List, Dict, date]


def _extended_bool(value) -> bool:
    return _BooleanModel(bool_value=value).bool_value


class _BooleanModel(BaseModel):
    bool_value: bool


def resolve(function: ValidResolvers, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]):
    if function is None or isinstance(function, str):
        return function

    if isinstance(function, (int, float, date, bool, IPv4Network, IPv6Network)):
        return str(function)

    if isinstance(function, list):
        result = []
        for entry in function:
            resolved_value = resolve(entry, params, mappings, conditions)
            if resolved_value != AWS_NOVALUE:
                result.append(resolved_value)
        return result

    if isinstance(function, dict):
        if is_resolvable_dict(function):
            function_name = next(iter(function))
            function_resolver = FUNCTION_MAPPINGS[function_name]
            return function_resolver(function[function_name], params, mappings, conditions)

        result = {}
        for k, v in function.items():
            resolved_value = resolve(v, params, mappings, conditions)
            if resolved_value != AWS_NOVALUE:
                result[k] = resolved_value
        return result

    raise ValueError(f"Not supported type: {type(function)}")


def resolve_ref(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> str:
    resolved_ref = resolve(function_body, params, mappings, conditions)
    if resolved_ref in params:
        return params[resolved_ref]
    else:
        logger.warning(f"Using `UNDEFINED_PARAM_{resolved_ref}` for {resolved_ref}. Original value wasn't available.")
        return f"UNDEFINED_PARAM_{resolved_ref}"


def resolve_join(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> str:
    delimiter, list_values = function_body
    resolved_delimiter = resolve(delimiter, params, mappings, conditions)
    resolved_list = resolve(list_values, params, mappings, conditions)
    return resolved_delimiter.join(str(e) for e in resolved_list)


def resolve_find_in_map(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]):
    map_name, top_level_key, second_level_key = function_body
    map_name = resolve(map_name, params, mappings, conditions)
    top_level_key = resolve(top_level_key, params, mappings, conditions)
    second_level_key = resolve(second_level_key, params, mappings, conditions)

    resolved_mapping = mappings.get(map_name, {}).get(top_level_key, {}).get(second_level_key)
    if resolved_mapping:
        return resolved_mapping
    else:
        logger.warning(
            f"Using `UNDEFINED_MAPPING_{map_name}_{top_level_key}_{second_level_key}` for {[map_name, top_level_key, second_level_key]}. Original value wasn't available."
        )
        return f"UNDEFINED_MAPPING_{map_name}_{top_level_key}_{second_level_key}"


def resolve_sub(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> str:
    replacements = params
    # Whenever we receive a list, first parameter is a text and the second one is a dict with custom replacements.
    # Whenever we receive a string, we need to resolve inlined variables
    if isinstance(function_body, list):
        text, custom_replacements = function_body
        replacements.update(resolve(custom_replacements, params, mappings, conditions))
    else:
        text = function_body
    for match in CONTAINS_CF_PARAM.findall(text):
        match_param = match[2:-1]  # Remove ${ and trailing }
        if match_param in replacements:
            value = resolve(replacements[match_param], params, mappings, conditions)
            text = text.replace(match, str(value))
    return text


def resolve_select(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]):
    index, list_values = function_body
    resolved_index = int(resolve(index, params, mappings, conditions))
    resolved_list = resolve(list_values, params, mappings, conditions)
    return resolved_list[resolved_index]


def resolve_split(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> List[str]:
    delimiter, source_string = function_body
    resolved_delimiter = resolve(delimiter, params, mappings, conditions)
    resolved_source_string = resolve(source_string, params, mappings, conditions)
    return resolved_source_string.split(resolved_delimiter)


def resolve_if(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> str:
    condition, true_section, false_section = function_body
    resolved_funct = resolve({"Condition": condition}, params, mappings, conditions)
    resolved_funct = _extended_bool(resolved_funct)
    if resolved_funct:
        return resolve(true_section, params, mappings, conditions)
    else:
        return resolve(false_section, params, mappings, conditions)


def resolve_and(function_body: List, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> bool:
    return all(_extended_bool(resolve(part, params, mappings, conditions)) for part in function_body)


def resolve_or(function_body: List, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> bool:
    return any(_extended_bool(resolve(part, params, mappings, conditions)) for part in function_body)


def resolve_not(function_body: List, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> bool:
    return not _extended_bool(resolve(function_body[0], params, mappings, conditions))


def resolve_equals(function_body: List, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> bool:
    part_1, part_2 = function_body
    return resolve(part_1, params, mappings, conditions) == resolve(part_2, params, mappings, conditions)


def resolve_base64(function_body: str, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> str:
    resolved_string = resolve(function_body, params, mappings, conditions)
    return str(b64encode(resolved_string.encode("utf-8")), "utf-8")


def resolve_get_attr(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> str:
    # TODO: Implement.
    logger.warning(f"`Fn::GetAtt` resolver not implemented, returning `GETATT`")
    return "GETATT"


def resolve_get_azs(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> str:
    # TODO: Implement.
    logger.warning(f"`Fn::GetAZs` resolver not implemented, returning `GETAZS`")
    return "GETAZS"


def resolve_condition(function_body, params: Dict, mappings: Dict[str, Dict], conditions: Dict[str, bool]) -> bool:
    # TODO: Implement resolve conditions inside resources
    return conditions.get(function_body, False)


FUNCTION_MAPPINGS = {
    "Condition": resolve_condition,
    "Fn::And": resolve_and,
    "Fn::Base64": resolve_base64,
    "Fn::Equals": resolve_equals,
    "Fn::FindInMap": resolve_find_in_map,
    "Fn::GetAtt": resolve_get_attr,
    "Fn::GetAZs": resolve_get_azs,
    "Fn::If": resolve_if,
    "Fn::ImportValue": resolve_ref,
    "Fn::Join": resolve_join,
    "Fn::Not": resolve_not,
    "Fn::Or": resolve_or,
    "Fn::Select": resolve_select,
    "Fn::Split": resolve_split,
    "Fn::Sub": resolve_sub,
    "Ref": resolve_ref,
}
