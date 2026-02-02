"""
Validators for CloudFormation intrinsic functions.

Based on AWS documentation:
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html
"""

from typing import Any, Dict, Optional, Tuple


def _is_valid_function_or_string(value: Any) -> bool:
    """Check if value is a string or a valid intrinsic function dict."""
    if isinstance(value, str):
        return True
    if isinstance(value, dict) and len(value) == 1:
        key = next(iter(value))
        return key in FUNCTION_VALIDATORS or key == "Condition"
    return False


def _is_valid_function_or_value(value: Any) -> bool:
    """Check if value is any valid value or a valid intrinsic function dict."""
    if value is None:
        return True
    if isinstance(value, (str, int, float, bool, list)):
        return True
    if isinstance(value, dict):
        if len(value) == 1:
            key = next(iter(value))
            return key in FUNCTION_VALIDATORS or key == "Condition"
        # Could be a regular dict/object
        return True
    return False


def validate_ref(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Ref intrinsic function.

    Format: {"Ref": "logicalName"}

    The value must be a string (logical name of a resource, parameter, or pseudo parameter).
    """
    if not isinstance(value, str):
        return False, f"Ref value must be a string, got {type(value).__name__}"
    if not value:
        return False, "Ref value cannot be empty"
    return True, None


def validate_fn_base64(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Base64 intrinsic function.

    Format: {"Fn::Base64": "valueToEncode"}
           {"Fn::Base64": {"Ref": "..."}}

    The value must be a string or a function that resolves to a string.
    """
    if not _is_valid_function_or_string(value):
        return False, f"Fn::Base64 value must be a string or function, got {type(value).__name__}"
    return True, None


def validate_fn_and(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::And intrinsic function.

    Format: {"Fn::And": [condition1, condition2, ...]}

    Must be a list of 2-10 conditions.
    """
    if not isinstance(value, list):
        return False, f"Fn::And value must be a list, got {type(value).__name__}"
    if len(value) < 2 or len(value) > 10:
        return False, f"Fn::And requires 2-10 conditions, got {len(value)}"
    return True, None


def validate_fn_equals(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Equals intrinsic function.

    Format: {"Fn::Equals": [value1, value2]}

    Must be a list of exactly 2 values.
    """
    if not isinstance(value, list):
        return False, f"Fn::Equals value must be a list, got {type(value).__name__}"
    if len(value) != 2:
        return False, f"Fn::Equals requires exactly 2 values, got {len(value)}"
    return True, None


def validate_fn_if(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::If intrinsic function.

    Format: {"Fn::If": [condition_name, value_if_true, value_if_false]}

    Must be a list of exactly 3 elements.
    """
    if not isinstance(value, list):
        return False, f"Fn::If value must be a list, got {type(value).__name__}"
    if len(value) != 3:
        return False, f"Fn::If requires exactly 3 values (condition, true_value, false_value), got {len(value)}"
    return True, None


def validate_fn_not(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Not intrinsic function.

    Format: {"Fn::Not": [condition]}

    Must be a list with exactly 1 condition.
    """
    if not isinstance(value, list):
        return False, f"Fn::Not value must be a list, got {type(value).__name__}"
    if len(value) != 1:
        return False, f"Fn::Not requires exactly 1 condition, got {len(value)}"
    return True, None


def validate_fn_or(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Or intrinsic function.

    Format: {"Fn::Or": [condition1, condition2, ...]}

    Must be a list of 2-10 conditions.
    """
    if not isinstance(value, list):
        return False, f"Fn::Or value must be a list, got {type(value).__name__}"
    if len(value) < 2 or len(value) > 10:
        return False, f"Fn::Or requires 2-10 conditions, got {len(value)}"
    return True, None


def validate_fn_find_in_map(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::FindInMap intrinsic function.

    Format: {"Fn::FindInMap": [MapName, TopLevelKey, SecondLevelKey]}

    Must be a list of exactly 3 elements.
    """
    if not isinstance(value, list):
        return False, f"Fn::FindInMap value must be a list, got {type(value).__name__}"
    if len(value) != 3:
        return False, f"Fn::FindInMap requires exactly 3 values (map, key1, key2), got {len(value)}"
    return True, None


def validate_fn_get_att(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::GetAtt intrinsic function.

    Format: {"Fn::GetAtt": [logicalNameOfResource, attributeName]}
            {"Fn::GetAtt": "logicalNameOfResource.attributeName"}

    Can be a list of 2 strings or a dot-separated string.
    """
    if isinstance(value, str):
        if "." not in value:
            return False, "Fn::GetAtt string format must contain a dot (resource.attribute)"
        return True, None
    if isinstance(value, list):
        if len(value) != 2:
            return False, f"Fn::GetAtt list must have exactly 2 elements, got {len(value)}"
        return True, None
    return False, f"Fn::GetAtt value must be a string or list, got {type(value).__name__}"


def validate_fn_get_azs(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::GetAZs intrinsic function.

    Format: {"Fn::GetAZs": "region"}
            {"Fn::GetAZs": {"Ref": "AWS::Region"}}
            {"Fn::GetAZs": ""}  (empty string = current region)

    Value must be a string (region name or empty) or a function.
    """
    if isinstance(value, str):
        return True, None
    if isinstance(value, dict) and len(value) == 1:
        return True, None
    return False, f"Fn::GetAZs value must be a string or function, got {type(value).__name__}"


def validate_fn_import_value(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::ImportValue intrinsic function.

    Format: {"Fn::ImportValue": "sharedValueToImport"}
            {"Fn::ImportValue": {"Fn::Sub": "..."}}

    Value must be a string or a function that resolves to a string.
    """
    if not _is_valid_function_or_string(value):
        return False, f"Fn::ImportValue value must be a string or function, got {type(value).__name__}"
    return True, None


def validate_fn_join(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Join intrinsic function.

    Format: {"Fn::Join": ["delimiter", [list, of, values]]}

    Must be a list of exactly 2 elements: delimiter (string) and list of values.
    """
    if not isinstance(value, list):
        return False, f"Fn::Join value must be a list, got {type(value).__name__}"
    if len(value) != 2:
        return False, f"Fn::Join requires exactly 2 values (delimiter, list), got {len(value)}"
    delimiter, values_list = value
    if not isinstance(delimiter, str):
        return False, f"Fn::Join delimiter must be a string, got {type(delimiter).__name__}"
    if not isinstance(values_list, list) and not isinstance(values_list, dict):
        return False, f"Fn::Join second argument must be a list or function, got {type(values_list).__name__}"
    return True, None


def validate_fn_select(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Select intrinsic function.

    Format: {"Fn::Select": [index, listOfObjects]}

    Must be a list of exactly 2 elements: index (string/int or function) and list.
    """
    if not isinstance(value, list):
        return False, f"Fn::Select value must be a list, got {type(value).__name__}"
    if len(value) != 2:
        return False, f"Fn::Select requires exactly 2 values (index, list), got {len(value)}"
    return True, None


def validate_fn_split(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Split intrinsic function.

    Format: {"Fn::Split": ["delimiter", "source string"]}

    Must be a list of exactly 2 elements.
    """
    if not isinstance(value, list):
        return False, f"Fn::Split value must be a list, got {type(value).__name__}"
    if len(value) != 2:
        return False, f"Fn::Split requires exactly 2 values (delimiter, string), got {len(value)}"
    delimiter = value[0]
    if not isinstance(delimiter, str):
        return False, f"Fn::Split delimiter must be a string, got {type(delimiter).__name__}"
    return True, None


def validate_fn_sub(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Fn::Sub intrinsic function.

    Format: {"Fn::Sub": "string with ${variables}"}
            {"Fn::Sub": ["string with ${variables}", {var: value, ...}]}

    Can be a string or a list of [string, dict].
    """
    if isinstance(value, str):
        return True, None
    if isinstance(value, list):
        if len(value) != 2:
            return False, f"Fn::Sub list format requires exactly 2 values (string, vars), got {len(value)}"
        template_string, variables = value
        if not isinstance(template_string, str):
            return False, f"Fn::Sub template must be a string, got {type(template_string).__name__}"
        if not isinstance(variables, dict):
            return False, f"Fn::Sub variables must be a dict, got {type(variables).__name__}"
        return True, None
    return False, f"Fn::Sub value must be a string or list, got {type(value).__name__}"


def validate_condition(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate Condition intrinsic function.

    Format: {"Condition": "conditionName"}

    Value must be a string (name of a condition).
    """
    if not isinstance(value, str):
        return False, f"Condition value must be a string, got {type(value).__name__}"
    if not value:
        return False, "Condition value cannot be empty"
    return True, None


# Mapping of function names to their validators
FUNCTION_VALIDATORS: Dict[str, Any] = {
    "Ref": validate_ref,
    "Fn::Base64": validate_fn_base64,
    "Fn::And": validate_fn_and,
    "Fn::Equals": validate_fn_equals,
    "Fn::If": validate_fn_if,
    "Fn::Not": validate_fn_not,
    "Fn::Or": validate_fn_or,
    "Fn::FindInMap": validate_fn_find_in_map,
    "Fn::GetAtt": validate_fn_get_att,
    "Fn::GetAZs": validate_fn_get_azs,
    "Fn::ImportValue": validate_fn_import_value,
    "Fn::Join": validate_fn_join,
    "Fn::Select": validate_fn_select,
    "Fn::Split": validate_fn_split,
    "Fn::Sub": validate_fn_sub,
    "Condition": validate_condition,
}


def validate_intrinsic_function(function_dict: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate a CloudFormation intrinsic function dictionary.

    Args:
        function_dict: A dictionary with exactly one key (the function name)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(function_dict, dict):
        return False, f"Expected dict, got {type(function_dict).__name__}"

    if len(function_dict) != 1:
        return False, f"Intrinsic function must have exactly 1 key, got {len(function_dict)}"

    function_name = next(iter(function_dict))
    function_value = function_dict[function_name]

    if function_name not in FUNCTION_VALIDATORS:
        return False, f"Unknown intrinsic function: {function_name}"

    validator = FUNCTION_VALIDATORS[function_name]
    return validator(function_value)
