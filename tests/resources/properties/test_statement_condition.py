from datetime import datetime
from ipaddress import IPv4Network
from typing import Any, Dict, Tuple, Union

import pytest

from pycfmodel.model.resources.properties.statement_condition import (
    StatementCondition,
    StatementConditionBuildEvaluatorError,
    build_evaluator,
    build_root_evaluator,
)
from pycfmodel.resolver import resolve


def datetime_in_the_present():
    return datetime(2000, 1, 1, 0, 0)


def datetime_in_the_past():
    return datetime(1990, 1, 1, 0, 0)


def datetime_in_the_future():
    return datetime(2010, 1, 1, 0, 0)


def test_all_possible_conditions():
    # Based on https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html
    all_operators = set()
    for operator in [
        "ArnEquals",
        "ArnLike",
        "ArnNotEquals",
        "ArnNotLike",
        "Bool",
        "BinaryEquals",
        "DateEquals",
        "DateNotEquals",
        "DateLessThan",
        "DateLessThanEquals",
        "DateGreaterThan",
        "DateGreaterThanEquals",
        "IpAddress",
        "NotIpAddress",
        "NumericEquals",
        "NumericNotEquals",
        "NumericLessThan",
        "NumericLessThanEquals",
        "NumericGreaterThan",
        "NumericGreaterThanEquals",
        "StringEquals",
        "StringNotEquals",
        "StringEqualsIgnoreCase",
        "StringNotEqualsIgnoreCase",
        "StringLike",
        "StringNotLike",
    ]:
        all_operators.add(operator)
        all_operators.add(f"{operator}IfExists")

    # Null
    # Null is not compatible with IfExists
    all_operators.add("Null")

    # For(Any/All)Values
    for operator in all_operators.copy():
        all_operators.add(f"ForAllValues{operator}")
        all_operators.add(f"ForAnyValue{operator}")

    implemented_operators = sorted(StatementCondition.model_json_schema()["properties"].keys())
    assert implemented_operators == sorted(all_operators)


def test_statement_condition_remove_colon():
    assert StatementCondition.model_validate(
        {
            "ForAllValues:ArnEqualsIfExists": {"patata_1": "test_1"},
            "ForAnyValue:ArnEquals": {"patata_2": ["test_2", "test_3"]},
        }
    ) == StatementCondition(
        ForAllValuesArnEqualsIfExists={"patata_1": "test_1"}, ForAnyValueArnEquals={"patata_2": ["test_2", "test_3"]}
    )


def test_eval_is_built_only_if_called():
    condition = StatementCondition()
    assert condition._eval is None
    condition.eval({})
    assert condition._eval is not None


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("Bool", "patata", True, {"patata": True}, True),
        ("Bool", "patata", True, {"patata": False}, False),
        ("Bool", "patata", False, {"patata": True}, False),
        ("Bool", "patata", False, {"patata": False}, True),
    ],
)
def test_build_evaluator_bool(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("IpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Network("203.0.113.12")}, True),
        ("IpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Network("10.1.1.1")}, False),
        ("IpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Network("203.0.113.10")}, True),
        ("IpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Network("10.1.1.1")}, False),
        ("IpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Network("203.0.113.10")}, False),
        ("IpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Network("172.16.0.13")}, True),
        ("IpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Network("172.16.0.0/12")}, True),
        ("IpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Network("203.0.113.10/32")}, False),
    ],
)
def test_build_evaluator_ip_address(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("NotIpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Network("203.0.113.12")}, False),
        ("NotIpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Network("10.1.1.1")}, True),
        ("NotIpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Network("203.0.113.10")}, False),
        ("NotIpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Network("10.1.1.1")}, True),
        ("NotIpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Network("203.0.113.10")}, True),
        ("NotIpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Network("172.16.0.13")}, False),
        ("NotIpAddress", "patata", IPv4Network("172.0.0.0/8"), {"patata": IPv4Network("172.0.0.0/8")}, False),
    ],
)
def test_build_evaluator_not_ip_address(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("Null", "patata", True, {"patata": 1}, True),
        ("Null", "patata", True, {}, False),
        ("Null", "patata", False, {"patata": 1}, False),
        ("Null", "patata", False, {}, True),
    ],
)
def test_build_evaluator_null(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [("NumericEquals", "patata", 1, {"patata": 1}, True), ("NumericEquals", "patata", 1, {"patata": 2}, False)],
)
def test_build_evaluator_numeric_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [("NumericNotEquals", "patata", 1, {"patata": 1}, False), ("NumericNotEquals", "patata", 1, {"patata": 2}, True)],
)
def test_build_evaluator_numeric_not_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("NumericLessThan", "patata", 1, {"patata": 1}, False),
        ("NumericLessThan", "patata", 1, {"patata": 2}, False),
        ("NumericLessThan", "patata", 2, {"patata": 1}, True),
    ],
)
def test_build_evaluator_numeric_less_than(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("NumericLessThanEquals", "patata", 1, {"patata": 1}, True),
        ("NumericLessThanEquals", "patata", 1, {"patata": 2}, False),
        ("NumericLessThanEquals", "patata", 2, {"patata": 1}, True),
    ],
)
def test_build_evaluator_numeric_less_than_equals(
    function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool
):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("NumericGreaterThan", "patata", 2, {"patata": 2}, False),
        ("NumericGreaterThan", "patata", 2, {"patata": 1}, False),
        ("NumericGreaterThan", "patata", 1, {"patata": 2}, True),
    ],
)
def test_build_evaluator_numeric_greater_than(
    function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool
):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("NumericGreaterThanEquals", "patata", 2, {"patata": 2}, True),
        ("NumericGreaterThanEquals", "patata", 2, {"patata": 1}, False),
        ("NumericGreaterThanEquals", "patata", 1, {"patata": 2}, True),
    ],
)
def test_build_evaluator_numeric_greater_than_equals(
    function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool
):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("DateEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, True),
        ("DateEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_past()}, False),
    ],
)
def test_build_evaluator_date_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("DateNotEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, False),
        ("DateNotEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_past()}, True),
    ],
)
def test_build_evaluator_date_not_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("DateLessThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, False),
        ("DateLessThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, False),
        ("DateLessThan", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, True),
    ],
)
def test_build_evaluator_date_less_than(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("DateLessThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, True),
        ("DateLessThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, False),
        ("DateLessThanEquals", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, True),
    ],
)
def test_build_evaluator_date_less_than_equals(
    function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool
):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("DateGreaterThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, False),
        ("DateGreaterThan", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, False),
        ("DateGreaterThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, True),
    ],
)
def test_build_evaluator_date_greater_than(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("DateGreaterThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, True),
        ("DateGreaterThanEquals", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, False),
        ("DateGreaterThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, True),
    ],
)
def test_build_evaluator_date_greater_than_equals(
    function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool
):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("StringEquals", "patata", "aaaaa", {"patata": "aaaaa"}, True),
        ("StringEquals", "patata", "AAAAA", {"patata": "AAAAA"}, True),
        ("StringEquals", "patata", "AaAaA", {"patata": "AaAaA"}, True),
        ("StringEquals", "patata", "AAAAA", {"patata": "aaaaa"}, False),
        ("StringEquals", "patata", "aaaaa", {"patata": "AAAAA"}, False),
        ("StringEquals", "patata", "aAaAa", {"patata": "AaAaA"}, False),
        ("StringEquals", "patata", "aaaaa", {"patata": "bbbbb"}, False),
    ],
)
def test_build_evaluator_string_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("StringNotEquals", "patata", "aaaaa", {"patata": "aaaaa"}, False),
        ("StringNotEquals", "patata", "AAAAA", {"patata": "AAAAA"}, False),
        ("StringNotEquals", "patata", "AaAaA", {"patata": "AaAaA"}, False),
        ("StringNotEquals", "patata", "AAAAA", {"patata": "aaaaa"}, True),
        ("StringNotEquals", "patata", "aaaaa", {"patata": "AAAAA"}, True),
        ("StringNotEquals", "patata", "aAaAa", {"patata": "AaAaA"}, True),
        ("StringNotEquals", "patata", "aaaaa", {"patata": "bbbbb"}, True),
    ],
)
def test_build_evaluator_string_not_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("StringEqualsIgnoreCase", "patata", "aaaaa", {"patata": "aaaaa"}, True),
        ("StringEqualsIgnoreCase", "patata", "AAAAA", {"patata": "AAAAA"}, True),
        ("StringEqualsIgnoreCase", "patata", "AaAaA", {"patata": "AaAaA"}, True),
        ("StringEqualsIgnoreCase", "patata", "AAAAA", {"patata": "aaaaa"}, True),
        ("StringEqualsIgnoreCase", "patata", "aaaaa", {"patata": "AAAAA"}, True),
        ("StringEqualsIgnoreCase", "patata", "aAaAa", {"patata": "AaAaA"}, True),
        ("StringEqualsIgnoreCase", "patata", "aaaaa", {"patata": "bbbbb"}, False),
    ],
)
def test_build_evaluator_string_equals_ignore_case(
    function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool
):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("StringNotEqualsIgnoreCase", "patata", "aaaaa", {"patata": "aaaaa"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "AAAAA", {"patata": "AAAAA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "AaAaA", {"patata": "AaAaA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "AAAAA", {"patata": "aaaaa"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "aaaaa", {"patata": "AAAAA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "aAaAa", {"patata": "AaAaA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "aaaaa", {"patata": "bbbbb"}, True),
    ],
)
def test_build_evaluator_string_not_equals_ignore_case(
    function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool
):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("StringLike", "patata", "aa*cc", {"patata": "aabcc"}, True),
        ("StringLike", "patata", "aa*cc", {"patata": "abbcc"}, False),
    ],
)
def test_build_evaluator_string_like(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("StringNotLike", "patata", "aa*cc", {"patata": "abbcc"}, True),
        ("StringNotLike", "patata", "aa*cc", {"patata": "aabcc"}, False),
    ],
)
def test_build_evaluator_string_not_like(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        (
            "ArnEquals",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance",
            {"patata": "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance"},
            True,
        ),
        (
            "ArnEquals",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/another_test_instance",
            {"patata": "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance"},
            False,
        ),
    ],
)
def test_build_evaluator_arn_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        (
            "ArnNotEquals",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance",
            {"patata": "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance"},
            False,
        ),
        (
            "ArnNotEquals",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/another_test_instance",
            {"patata": "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance"},
            True,
        ),
    ],
)
def test_build_evaluator_arn_not_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        (
            "ArnLike",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/*",
            {"patata": "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance"},
            True,
        ),
        (
            "ArnLike",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/*",
            {"patata": "arn:aws:ec2:eu-west-1:111122223333:instance/test_instance"},
            False,
        ),
    ],
)
def test_build_evaluator_arn_like(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        (
            "ArnNotLike",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/*",
            {"patata": "arn:aws:ec2:eu-west-1:111122223333:instance/test_instance"},
            True,
        ),
        (
            "ArnNotLike",
            "patata",
            "arn:aws:ec2:sa-east-1:111122223333:instance/*",
            {"patata": "arn:aws:ec2:sa-east-1:111122223333:instance/test_instance"},
            False,
        ),
    ],
)
def test_build_evaluator_arn_not_like(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        ("BinaryEquals", "patata", bytearray("AaAaA", "utf-8"), {"patata": bytearray("AaAaA", "utf-8")}, True),
        ("BinaryEquals", "patata", bytearray("AAAAA", "utf-8"), {"patata": bytearray("aaaaa", "utf-8")}, False),
    ],
)
def test_build_evaluator_binary_equals(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arguments, params, expected_output",
    [
        ("NumericEquals", {"patata": 1}, {"patata": 1}, True),
        ("NumericEquals", {"patata": 1}, {"patata": 2}, False),
        ("StringEquals", {"patata": ["1", "2", "3"]}, {"patata": ["2", "1"]}, True),
        ("StringEquals", {"patata": ["1", "2", "3"]}, {"patata": ["1", "3"]}, True),
        ("StringEquals", {"patata": "2"}, {"patata": ["2"]}, False),
        ("StringEquals", {"patata": "2"}, {"patata": ["2", "1"]}, False),
        ("StringEquals", {"patata": ["1", "3"]}, {"patata": ["4"]}, False),
        ("StringLike", {"patata": ["sky*"]}, {"patata": ["skyx", "skyscanner", "nope"]}, True),
        ("StringLike", {"patata": ["sky*"]}, {"patata": ["nopeskyx", "nopeskyscanner", "nope"]}, False),
        ("IpAddress", {"patata": [IPv4Network("203.0.113.0/24")]}, {"patata": IPv4Network("203.0.113.0/24")}, True),
        ("IpAddress", {"patata": [IPv4Network("203.0.113.0/24")]}, {"patata": [IPv4Network("203.0.113.0/24")]}, True),
        ("IpAddress", {"patata": ["vpce-123456"]}, {"patata": ["vpce-123456"]}, False),
        ("NotIpAddress", {"patata": ["vpce-123456"]}, {"patata": ["vpce-654321"]}, False),
        (
            "IpAddress",
            {"patata": [IPv4Network("203.0.113.0/24"), IPv4Network("103.0.113.0/24"), IPv4Network("85.0.113.0/24")]},
            {"patata": [IPv4Network("10.0.0.0/8")]},
            False,
        ),
    ],
)
def test_build_root_evaluator(function: str, arguments: Union[Dict, Tuple], params: Dict, expected_output: bool):
    node = build_root_evaluator(function, arguments)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arguments, params, expected_output",
    [
        ("NumericEqualsIfExists", {"patata": 1}, {"patata": 1}, True),
        ("NumericEqualsIfExists", {"patata": 1}, {"patata": 2}, False),
        ("NumericEqualsIfExists", {"patata": 1}, {}, True),
    ],
)
def test_build_root_evaluator_if_exists(
    function: str, arguments: Union[Dict, Tuple], params: Dict, expected_output: bool
):
    node = build_root_evaluator(function, arguments)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arguments, params, expected_output",
    [
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": 1}, True),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": 1}, True),
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": [1, 1]}, True),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": [1, 2]}, True),
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": 2}, False),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": [1, 4]}, False),
    ],
)
def test_build_root_evaluator_for_all_values(
    function: str, arguments: Union[Dict, Tuple], params: Dict, expected_output: bool
):
    node = build_root_evaluator(function, arguments)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arguments, params, expected_output",
    [
        ("ForAllValuesNumericEqualsIfExists", {"patata": 1}, {}, True),
        ("ForAllValuesNumericEqualsIfExists", {"patata": [1, 2, 3]}, {}, True),
        ("ForAllValuesNumericEqualsIfExists", {"patata": 1}, {"patata": 2}, False),
        ("ForAllValuesNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAllValuesNumericEqualsIfExists", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAllValuesNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": [1, 4]}, False),
    ],
)
def test_build_root_evaluator_for_all_values_if_exists(
    function: str, arguments: Union[Dict, Tuple], params: Dict, expected_output: bool
):
    node = build_root_evaluator(function, arguments)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arguments, params, expected_output",
    [
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": 1}, True),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": 1}, True),
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": [1, 2]}, True),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": [1, 2, 5, 6]}, True),
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": 2}, False),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": [4, 5]}, False),
    ],
)
def test_build_root_evaluator_for_any_value(
    function: str, arguments: Union[Dict, Tuple], params: Dict, expected_output: bool
):
    node = build_root_evaluator(function, arguments)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arguments, params, expected_output",
    [
        ("ForAnyValueNumericEqualsIfExists", {"patata": 1}, {}, True),
        ("ForAnyValueNumericEqualsIfExists", {"patata": [1, 2, 3]}, {}, True),
        ("ForAnyValueNumericEqualsIfExists", {"patata": 1}, {"patata": 2}, False),
        ("ForAnyValueNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAnyValueNumericEqualsIfExists", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAnyValueNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": [4, 5, 6]}, False),
    ],
)
def test_build_root_evaluator_for_any_value_if_exists(
    function: str, arguments: Union[Dict, Tuple], params: Dict, expected_output: bool
):
    node = build_root_evaluator(function, arguments)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "statement_condition, params, expected_output",
    [
        (StatementCondition(), {}, True),
        (StatementCondition(NumericEquals={"patata": 1}), {"patata": 1}, True),
        (StatementCondition(NumericEquals={"patata": 1}), {"patata": 2}, False),
        (
            StatementCondition(NumericEquals={"patata_1": 1}, StringEquals={"patata_2": "A"}),
            {"patata_1": 1, "patata_2": "A"},
            True,
        ),
        (
            StatementCondition(NumericEquals={"patata_1": 1}, StringEquals={"patata_2": "A"}),
            {"patata_1": 2, "patata_2": "A"},
            False,
        ),
        (
            StatementCondition(NumericEquals={"patata_1": 1}, StringEquals={"patata_2": "A"}),
            {"patata_1": 1, "patata_2": "B"},
            False,
        ),
        (
            StatementCondition(NumericEquals={"patata_1": 1}, StringEquals={"patata_2": "A"}),
            {"patata_1": 2, "patata_2": "B"},
            False,
        ),
    ],
)
def test_statement_condition_eval_all_conditions_are_true(
    statement_condition: StatementCondition, params: Dict, expected_output: bool
):
    assert statement_condition.eval(params) == expected_output


def test_statement_condition_without_resolving_raises_error():
    statement_condition_raw = {"StringLike": {"patata": {"Fn::Sub": "${ClusterId}*"}}}
    statement_condition = StatementCondition.model_validate(statement_condition_raw)
    with pytest.raises(StatementConditionBuildEvaluatorError):
        statement_condition.eval({"patata": "test_cluster"})


def test_statement_condition_with_resolver_works_fine():
    statement_condition_raw = {"StringLike": {"patata": {"Fn::Sub": "${ClusterId}*"}}}
    resolved_statement_condition_raw = resolve(statement_condition_raw, {"ClusterId": "test_cluster"}, {}, {})
    resolved_statement_condition = StatementCondition.model_validate(resolved_statement_condition_raw)
    assert resolved_statement_condition.eval({"patata": "test_cluster"}) is True
