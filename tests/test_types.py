import json
from ipaddress import IPv4Network, IPv6Network

import pytest
from pydantic import BaseModel, ValidationError

from pycfmodel.model.types import LooseIPv4Network, LooseIPv6Network


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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
    assert json.loads(exc_info.value.json()) == errors


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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
                    "url": "https://errors.pydantic.dev/2.7/v/value_error",
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
    assert json.loads(exc_info.value.json()) == errors
