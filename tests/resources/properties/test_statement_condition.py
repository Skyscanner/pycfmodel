from datetime import datetime
from ipaddress import IPv4Address, IPv4Network
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

    implemented_operators = sorted(StatementCondition.schema()["properties"].keys())
    assert implemented_operators == sorted(all_operators)


def test_statement_condition_remove_colon():
    assert StatementCondition.parse_obj(
        {
            "ForAllValues:ArnEqualsIfExists": {"patata_1": "test_1"},
            "ForAnyValue:ARNEquals": {"patata_2": ["test_2", "test_3"]},
        }
    ) == StatementCondition(
        ForAllValuesArnEqualsIfExists={"patata_1": "test_1"}, ForAnyValueARNEquals={"patata_2": ["test_2", "test_3"]}
    )


@pytest.mark.parametrize(
    "function, arg_a, arg_b, params, expected_output",
    [
        # Bool
        ("Bool", "patata", True, {"patata": True}, True),
        ("Bool", "patata", True, {"patata": False}, False),
        ("Bool", "patata", False, {"patata": True}, False),
        ("Bool", "patata", False, {"patata": False}, True),
        # IpAddress
        ("IpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Address("203.0.113.12")}, True),
        ("IpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Address("10.1.1.1")}, False),
        ("IpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Address("203.0.113.10")}, True),
        ("IpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Address("10.1.1.1")}, False),
        ("IpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Address("203.0.113.10")}, False),
        ("IpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Address("172.16.0.13")}, True),
        # NotIpAddress
        ("NotIpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Address("203.0.113.12")}, False),
        ("NotIpAddress", "patata", IPv4Network("203.0.113.0/24"), {"patata": IPv4Address("10.1.1.1")}, True),
        ("NotIpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Address("203.0.113.10")}, False),
        ("NotIpAddress", "patata", IPv4Network("203.0.113.10/32"), {"patata": IPv4Address("10.1.1.1")}, True),
        ("NotIpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Address("203.0.113.10")}, True),
        ("NotIpAddress", "patata", IPv4Network("172.16.0.0/12"), {"patata": IPv4Address("172.16.0.13")}, False),
        # Null
        ("Null", "patata", True, {"patata": 1}, True),
        ("Null", "patata", True, {}, False),
        ("Null", "patata", False, {"patata": 1}, False),
        ("Null", "patata", False, {}, True),
        # NumericEquals
        ("NumericEquals", "patata", 1, {"patata": 1}, True),
        ("NumericEquals", "patata", 1, {"patata": 2}, False),
        # NumericNotEquals
        ("NumericNotEquals", "patata", 1, {"patata": 1}, False),
        ("NumericNotEquals", "patata", 1, {"patata": 2}, True),
        # NumericLessThan
        ("NumericLessThan", "patata", 1, {"patata": 1}, False),
        ("NumericLessThan", "patata", 1, {"patata": 2}, False),
        ("NumericLessThan", "patata", 2, {"patata": 1}, True),
        # NumericLessThanEquals
        ("NumericLessThanEquals", "patata", 1, {"patata": 1}, True),
        ("NumericLessThanEquals", "patata", 1, {"patata": 2}, False),
        ("NumericLessThanEquals", "patata", 2, {"patata": 1}, True),
        # NumericGreaterThan
        ("NumericGreaterThan", "patata", 2, {"patata": 2}, False),
        ("NumericGreaterThan", "patata", 2, {"patata": 1}, False),
        ("NumericGreaterThan", "patata", 1, {"patata": 2}, True),
        # NumericGreaterThanEquals
        ("NumericGreaterThanEquals", "patata", 2, {"patata": 2}, True),
        ("NumericGreaterThanEquals", "patata", 2, {"patata": 1}, False),
        ("NumericGreaterThanEquals", "patata", 1, {"patata": 2}, True),
        # DateEquals
        ("DateEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, True),
        ("DateEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_past()}, False),
        # DateNotEquals
        ("DateNotEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, False),
        ("DateNotEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_past()}, True),
        # DateLessThan
        ("DateLessThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, False),
        ("DateLessThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, False),
        ("DateLessThan", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, True),
        # DateLessThanEquals
        ("DateLessThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, True),
        ("DateLessThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, False),
        ("DateLessThanEquals", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, True),
        # DateGreaterThan
        ("DateGreaterThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, False),
        ("DateGreaterThan", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, False),
        ("DateGreaterThan", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, True),
        # DateGreaterThanEquals
        ("DateGreaterThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_present()}, True),
        ("DateGreaterThanEquals", "patata", datetime_in_the_future(), {"patata": datetime_in_the_present()}, False),
        ("DateGreaterThanEquals", "patata", datetime_in_the_present(), {"patata": datetime_in_the_future()}, True),
        # StringEquals
        ("StringEquals", "patata", "aaaaa", {"patata": "aaaaa"}, True),
        ("StringEquals", "patata", "AAAAA", {"patata": "AAAAA"}, True),
        ("StringEquals", "patata", "AaAaA", {"patata": "AaAaA"}, True),
        ("StringEquals", "patata", "AAAAA", {"patata": "aaaaa"}, False),
        ("StringEquals", "patata", "aaaaa", {"patata": "AAAAA"}, False),
        ("StringEquals", "patata", "aAaAa", {"patata": "AaAaA"}, False),
        ("StringEquals", "patata", "aaaaa", {"patata": "bbbbb"}, False),
        # StringNotEquals
        ("StringNotEquals", "patata", "aaaaa", {"patata": "aaaaa"}, False),
        ("StringNotEquals", "patata", "AAAAA", {"patata": "AAAAA"}, False),
        ("StringNotEquals", "patata", "AaAaA", {"patata": "AaAaA"}, False),
        ("StringNotEquals", "patata", "AAAAA", {"patata": "aaaaa"}, True),
        ("StringNotEquals", "patata", "aaaaa", {"patata": "AAAAA"}, True),
        ("StringNotEquals", "patata", "aAaAa", {"patata": "AaAaA"}, True),
        ("StringNotEquals", "patata", "aaaaa", {"patata": "bbbbb"}, True),
        # StringEqualsIgnoreCase
        ("StringEqualsIgnoreCase", "patata", "aaaaa", {"patata": "aaaaa"}, True),
        ("StringEqualsIgnoreCase", "patata", "AAAAA", {"patata": "AAAAA"}, True),
        ("StringEqualsIgnoreCase", "patata", "AaAaA", {"patata": "AaAaA"}, True),
        ("StringEqualsIgnoreCase", "patata", "AAAAA", {"patata": "aaaaa"}, True),
        ("StringEqualsIgnoreCase", "patata", "aaaaa", {"patata": "AAAAA"}, True),
        ("StringEqualsIgnoreCase", "patata", "aAaAa", {"patata": "AaAaA"}, True),
        ("StringEqualsIgnoreCase", "patata", "aaaaa", {"patata": "bbbbb"}, False),
        # StringNotEqualsIgnoreCase
        ("StringNotEqualsIgnoreCase", "patata", "aaaaa", {"patata": "aaaaa"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "AAAAA", {"patata": "AAAAA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "AaAaA", {"patata": "AaAaA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "AAAAA", {"patata": "aaaaa"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "aaaaa", {"patata": "AAAAA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "aAaAa", {"patata": "AaAaA"}, False),
        ("StringNotEqualsIgnoreCase", "patata", "aaaaa", {"patata": "bbbbb"}, True),
        # StringLike
        ("StringLike", "patata", "aa*cc", {"patata": "aabcc"}, True),
        ("StringLike", "patata", "aa*cc", {"patata": "abbcc"}, False),
        # StringNotLike
        ("StringNotLike", "patata", "aa*cc", {"patata": "abbcc"}, True),
        ("StringNotLike", "patata", "aa*cc", {"patata": "aabcc"}, False),
        # ArnEquals
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
        # ArnNotEquals
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
        # ArnLike
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
        # ArnNotLike
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
        # BinaryEquals
        ("BinaryEquals", "patata", bytearray("AaAaA", "utf-8"), {"patata": bytearray("AaAaA", "utf-8")}, True),
        ("BinaryEquals", "patata", bytearray("AAAAA", "utf-8"), {"patata": bytearray("aaaaa", "utf-8")}, False),
    ],
)
def test_build_evaluator(function: str, arg_a: Any, arg_b: Any, params: Dict, expected_output: bool):
    node = build_evaluator(function, arg_a, arg_b)
    assert node(params) == expected_output


@pytest.mark.parametrize(
    "function, arguments, params, expected_output",
    [
        # Normal
        ("NumericEquals", {"patata": 1}, {"patata": 1}, True),
        ("NumericEquals", {"patata": 1}, {"patata": 2}, False),
        # ...IfExists
        ("NumericEqualsIfExists", {"patata": 1}, {"patata": 1}, True),
        ("NumericEqualsIfExists", {"patata": 1}, {"patata": 2}, False),
        ("NumericEqualsIfExists", {"patata": 1}, {}, True),
        # ForAllValues...
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": 1}, True),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": 1}, True),
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": [1, 1]}, True),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": [1, 2]}, True),
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": 2}, False),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAllValuesNumericEquals", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAllValuesNumericEquals", {"patata": [1, 2, 3]}, {"patata": [1, 4]}, False),
        # ForAllValues...IfExists
        ("ForAllValuesNumericEqualsIfExists", {"patata": 1}, {}, True),
        ("ForAllValuesNumericEqualsIfExists", {"patata": [1, 2, 3]}, {}, True),
        ("ForAllValuesNumericEqualsIfExists", {"patata": 1}, {"patata": 2}, False),
        ("ForAllValuesNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAllValuesNumericEqualsIfExists", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAllValuesNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": [1, 4]}, False),
        # ForAnyValue...
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": 1}, True),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": 1}, True),
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": [1, 2]}, True),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": [1, 2, 5, 6]}, True),
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": 2}, False),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAnyValueNumericEquals", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAnyValueNumericEquals", {"patata": [1, 2, 3]}, {"patata": [4, 5]}, False),
        # ForAnyValue...IfExists
        ("ForAnyValueNumericEqualsIfExists", {"patata": 1}, {}, True),
        ("ForAnyValueNumericEqualsIfExists", {"patata": [1, 2, 3]}, {}, True),
        ("ForAnyValueNumericEqualsIfExists", {"patata": 1}, {"patata": 2}, False),
        ("ForAnyValueNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": 4}, False),
        ("ForAnyValueNumericEqualsIfExists", {"patata": 1}, {"patata": [2, 3]}, False),
        ("ForAnyValueNumericEqualsIfExists", {"patata": [1, 2, 3]}, {"patata": [4, 5, 6]}, False),
    ],
)
def test_build_root_evaluator(function: str, arguments: Union[Dict, Tuple], params: Dict, expected_output: bool):
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
    statement_condition = StatementCondition.parse_obj(statement_condition_raw)
    with pytest.raises(StatementConditionBuildEvaluatorError):
        statement_condition.eval({"patata": "test_cluster"})


def test_statement_condition_with_resolver_works_fine():
    statement_condition_raw = {"StringLike": {"patata": {"Fn::Sub": "${ClusterId}*"}}}
    resolved_statement_condition_raw = resolve(statement_condition_raw, {"ClusterId": "test_cluster"}, {}, {})
    resolved_statement_condition = StatementCondition.parse_obj(resolved_statement_condition_raw)
    assert resolved_statement_condition.eval({"patata": "test_cluster"}) is True
