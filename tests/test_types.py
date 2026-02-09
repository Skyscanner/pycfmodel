import json
from ipaddress import IPv4Network, IPv6Network
from typing import Optional

import pytest
from pydantic import BaseModel, ValidationError

from pycfmodel.model.base import CustomModel, FunctionDict
from pycfmodel.model.types import LooseIPv4Network, LooseIPv6Network, ResolvableModel, ResolvableStr


def test_loose_ip_v4_network_type():
    class Model(BaseModel):
        ip_network: LooseIPv4Network

    model_schema = Model.model_json_schema()
    assert model_schema == {
        "title": "Model",
        "type": "object",
        "properties": {"ip_network": {"title": "Ip Network", "type": "string", "format": "looseipv4network"}},
        "required": ["ip_network"],
    }


def test_loose_ip_v6_network_type():
    class Model(BaseModel):
        ip_network: LooseIPv6Network

    model_schema = Model.model_json_schema()
    assert model_schema == {
        "title": "Model",
        "type": "object",
        "properties": {"ip_network": {"title": "Ip Network", "type": "string", "format": "looseipv6network"}},
        "required": ["ip_network"],
    }


@pytest.mark.parametrize(
    "value",
    [
        "192.168.0.0/24",
        "192.168.128.0/30",
        (2**32 - 1),  # no mask equals to mask /32
        b"\xff\xff\xff\xff",  # /32
        ("192.168.0.0", 24),
        (IPv4Network("192.168.0.0/24")),
    ],
)
def test_loose_ip_v4_network_success(value):
    class Model(BaseModel):
        ip: LooseIPv4Network = None

    assert Model(ip=value).ip == IPv4Network(value)


@pytest.mark.parametrize(
    "value",
    [
        "2001:db00::0/120",
        20_282_409_603_651_670_423_947_251_286_015,  # /128
        b"\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff",
        ("2001:db00::0", 120),
        (IPv6Network("2001:db00::0/120")),
    ],
)
def test_loose_ip_v6_network_success(value):
    class Model(BaseModel):
        ip: LooseIPv6Network = None

    assert Model(ip=value).ip == IPv6Network(value)


@pytest.mark.parametrize("value", ["213.174.214.100/27", "192.168.56.101/16", "192.0.2.1/24"])
def test_loose_ip_v4_is_not_strict(value):
    class Model(BaseModel):
        ip: LooseIPv4Network = None

    with pytest.raises(ValueError):
        IPv4Network(value, True)
    assert Model(ip=value).ip == IPv4Network(value, False)


@pytest.mark.parametrize(
    "value",
    ["2012::1234:abcd:ffff:c0a8:101/64", "2022::1234:abcd:ffff:c0a8:101/64", "2032::1234:abcd:ffff:c0a8:101/64"],
)
def test_loose_ip_v6_is_not_strict(value):
    class Model(BaseModel):
        ip: LooseIPv6Network = None

    with pytest.raises(ValueError):
        IPv6Network(value, True)
    assert Model(ip=value).ip == IPv6Network(value, False)


@pytest.mark.parametrize(
    "value,errors",
    [
        (
            "hello,world",
            [
                {
                    "ctx": {"error": ("Expected 4 octets in 'hello,world'")},
                    "input": "hello,world",
                    "loc": ["ip"],
                    "msg": "Value error, Expected 4 octets in 'hello,world'",
                    "type": "value_error",
                }
            ],
        ),
        (
            "192.168.0.1.1.1/24",
            [
                {
                    "ctx": {"error": ("Expected 4 octets in '192.168.0.1.1.1'")},
                    "input": "192.168.0.1.1.1/24",
                    "loc": ["ip"],
                    "msg": "Value error, Expected 4 octets in '192.168.0.1.1.1'",
                    "type": "value_error",
                }
            ],
        ),
        (
            -1,
            [
                {
                    "ctx": {"error": ("-1 (< 0) is not permitted as an IPv4 address")},
                    "input": -1,
                    "loc": ["ip"],
                    "msg": "Value error, -1 (< 0) is not permitted as an IPv4 address",
                    "type": "value_error",
                }
            ],
        ),
        (
            2**128 + 1,
            [
                {
                    "ctx": {
                        "error": (
                            "340282366920938463463374607431768211457 (>= 2**32) is not permitted as an IPv4 address"
                        )
                    },
                    "input": 340282366920938463463374607431768211457,
                    "loc": ["ip"],
                    "msg": "Value error, 340282366920938463463374607431768211457 (>= 2**32) is "
                    "not permitted as an IPv4 address",
                    "type": "value_error",
                }
            ],
        ),
        (
            "2001:db00::1/120",
            [
                {
                    "ctx": {"error": ("Expected 4 octets in '2001:db00::1'")},
                    "input": "2001:db00::1/120",
                    "loc": ["ip"],
                    "msg": "Value error, Expected 4 octets in '2001:db00::1'",
                    "type": "value_error",
                }
            ],
        ),
    ],
)
def test_loose_ip_v4_network_fails(value, errors):
    class Model(BaseModel):
        ip: LooseIPv4Network = None

    with pytest.raises(ValidationError) as exc_info:
        Model(ip=value)
    actual_errors = json.loads(exc_info.value.json())
    # Remove 'url' field from comparison as it contains pydantic version
    for error in actual_errors:
        error.pop("url", None)
    assert actual_errors == errors


@pytest.mark.parametrize(
    "value,errors",
    [
        (
            "hello,world",
            [
                {
                    "ctx": {"error": ("At least 3 parts expected in 'hello,world'")},
                    "input": "hello,world",
                    "loc": ["ip"],
                    "msg": "Value error, At least 3 parts expected in 'hello,world'",
                    "type": "value_error",
                }
            ],
        ),
        (
            "192.168.0.1.1.1/24",
            [
                {
                    "ctx": {"error": ("At least 3 parts expected in '192.168.0.1.1.1'")},
                    "input": "192.168.0.1.1.1/24",
                    "loc": ["ip"],
                    "msg": "Value error, At least 3 parts expected in '192.168.0.1.1.1'",
                    "type": "value_error",
                }
            ],
        ),
        (
            -1,
            [
                {
                    "ctx": {"error": "-1 (< 0) is not permitted as an IPv6 address"},
                    "input": -1,
                    "loc": ["ip"],
                    "msg": "Value error, -1 (< 0) is not permitted as an IPv6 address",
                    "type": "value_error",
                }
            ],
        ),
        (
            2**128 + 1,
            [
                {
                    "ctx": {
                        "error": (
                            "340282366920938463463374607431768211457 (>= 2**128) is not permitted as an IPv6 address"
                        )
                    },
                    "input": 340282366920938463463374607431768211457,
                    "loc": ["ip"],
                    "msg": "Value error, 340282366920938463463374607431768211457 (>= 2**128) is "
                    "not permitted as an IPv6 address",
                    "type": "value_error",
                }
            ],
        ),
        (
            "192.168.0.1/24",
            [
                {
                    "ctx": {"error": ("At least 3 parts expected in '192.168.0.1'")},
                    "input": "192.168.0.1/24",
                    "loc": ["ip"],
                    "msg": "Value error, At least 3 parts expected in '192.168.0.1'",
                    "type": "value_error",
                }
            ],
        ),
    ],
)
def test_loose_ip_v6_network_fails(value, errors):
    class Model(BaseModel):
        ip: LooseIPv6Network = None

    with pytest.raises(ValidationError) as exc_info:
        Model(ip=value)
    actual_errors = json.loads(exc_info.value.json())
    # Remove 'url' field from comparison as it contains pydantic version
    for error in actual_errors:
        error.pop("url", None)
    assert actual_errors == errors


# ResolvableModel tests


class NestedModel(CustomModel):
    """A nested model for testing ResolvableModel."""

    field1: ResolvableStr
    field2: Optional[ResolvableStr] = None


ResolvableNestedModel = ResolvableModel(NestedModel)


class ParentModel(CustomModel):
    """A parent model that uses ResolvableModel for nested types."""

    nested: Optional[ResolvableNestedModel] = None
    nested_required: ResolvableNestedModel


def test_resolvable_model_accepts_dict():
    """ResolvableModel should accept a dict and convert it to the model."""
    result = ParentModel(
        nested={"field1": "value1", "field2": "value2"},
        nested_required={"field1": "required_value"},
    )

    assert isinstance(result.nested, NestedModel)
    assert result.nested.field1 == "value1"
    assert result.nested.field2 == "value2"
    assert isinstance(result.nested_required, NestedModel)
    assert result.nested_required.field1 == "required_value"


def test_resolvable_model_accepts_model_instance():
    """ResolvableModel should accept an existing model instance."""
    nested_instance = NestedModel(field1="value1")
    result = ParentModel(nested=nested_instance, nested_required=nested_instance)

    assert result.nested is nested_instance
    assert result.nested_required is nested_instance


def test_resolvable_model_accepts_ref():
    """ResolvableModel should accept a Ref intrinsic function."""
    result = ParentModel(
        nested={"Ref": "NestedParam"},
        nested_required={"Ref": "RequiredNestedParam"},
    )

    assert isinstance(result.nested, FunctionDict)
    assert result.nested.Ref == "NestedParam"
    assert isinstance(result.nested_required, FunctionDict)
    assert result.nested_required.Ref == "RequiredNestedParam"


def test_resolvable_model_accepts_fn_sub():
    """ResolvableModel should accept Fn::Sub intrinsic function."""
    result = ParentModel(
        nested={"Fn::Sub": "${Param}"},
        nested_required={"Fn::Sub": "required-${Param}"},
    )

    assert isinstance(result.nested, FunctionDict)
    assert result.nested.model_dump()["Fn::Sub"] == "${Param}"
    assert isinstance(result.nested_required, FunctionDict)


def test_resolvable_model_accepts_fn_if():
    """ResolvableModel should accept Fn::If intrinsic function."""
    result = ParentModel(
        nested={"Fn::If": ["Condition", {"field1": "value1"}, {"field1": "value2"}]},
        nested_required={"Fn::If": ["Condition", {"field1": "v1"}, {"field1": "v2"}]},
    )

    assert isinstance(result.nested, FunctionDict)
    assert isinstance(result.nested_required, FunctionDict)


def test_resolvable_model_accepts_none_for_optional():
    """ResolvableModel with Optional should accept None."""
    result = ParentModel(nested=None, nested_required={"field1": "value"})

    assert result.nested is None
    assert isinstance(result.nested_required, NestedModel)


def test_resolvable_model_rejects_invalid_dict():
    """ResolvableModel should reject a dict missing required fields."""
    with pytest.raises(ValidationError) as exc_info:
        ParentModel(nested={"field2": "only_optional"}, nested_required={"field1": "value"})

    errors = json.loads(exc_info.value.json())
    assert any("field1" in str(e) for e in errors)


def test_resolvable_model_rejects_invalid_type():
    """ResolvableModel should reject invalid types like strings or lists."""
    with pytest.raises(ValidationError):
        ParentModel(nested="invalid_string", nested_required={"field1": "value"})

    with pytest.raises(ValidationError):
        ParentModel(nested=["invalid", "list"], nested_required={"field1": "value"})


def test_resolvable_model_serialization():
    """ResolvableModel should serialize correctly."""
    result = ParentModel(
        nested={"field1": "value1", "field2": "value2"},
        nested_required={"field1": "required_value"},
    )

    dumped = result.model_dump()
    assert dumped["nested"] == {"field1": "value1", "field2": "value2"}
    assert dumped["nested_required"] == {"field1": "required_value", "field2": None}


def test_resolvable_model_serialization_with_intrinsic():
    """ResolvableModel with intrinsic functions should serialize correctly."""
    result = ParentModel(
        nested={"Ref": "NestedParam"},
        nested_required={"Ref": "RequiredParam"},
    )

    dumped = result.model_dump()
    assert dumped["nested"] == {"Ref": "NestedParam"}
    assert dumped["nested_required"] == {"Ref": "RequiredParam"}
