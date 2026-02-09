from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network

import pytest

from pycfmodel.model.base import FunctionDict
from pycfmodel.model.generic import Generic, _Auxiliar
from pycfmodel.model.resources.properties.tag import Tag


def test_recursive():
    value = {"a": {"b": {"c": 1}}}
    generic_value = Generic.model_validate(value)
    assert generic_value == Generic(a=Generic(b=Generic(c=1)))
    assert generic_value.model_dump() == value


@pytest.mark.parametrize(
    "raw_value, parsed_value",
    [
        # FunctionDict
        ({"Fn::ImportValue": "abc"}, FunctionDict(**{"Fn::ImportValue": "abc"})),
        ([{"Fn::ImportValue": "abc"}], [FunctionDict(**{"Fn::ImportValue": "abc"})]),
        # Properties
        ({"Key": "test", "Value": "potatoe"}, Tag(Key="test", Value="potatoe")),
        ([{"Key": "test", "Value": "potatoe"}], [Tag(Key="test", Value="potatoe")]),
        # ResolvableBoolOrList
        (True, True),
        ([True], [True]),
        ("true", True),
        (["true"], [True]),
        ("True", True),
        (["True"], [True]),
        ("TRUE", True),
        (["TRUE"], [True]),
        # ResolvableIntOrList
        ("1", 1),
        (["1"], [1]),
        # ResolvableDatetimeOrList
        ("2011-11-04T00:05:23", datetime(2011, 11, 4, 0, 5, 23)),
        (["2011-11-04T00:05:23"], [datetime(2011, 11, 4, 0, 5, 23)]),
        # ResolvableDateOrList
        ("2019-12-04", date(2019, 12, 4)),
        (["2019-12-04"], [date(2019, 12, 4)]),
        # ResolvableIPOrList
        ("116.202.65.160/32", IPv4Network("116.202.65.160/32")),
        (["116.202.65.160/32"], [IPv4Network("116.202.65.160/32")]),
        ("2001:db00::0/120", IPv6Network("2001:db00::0/120")),
        (["2001:db00::0/120"], [IPv6Network("2001:db00::0/120")]),
        # ResolvableArnOrList
        ("arn:aws:iam::123456789012:user/test-user", "arn:aws:iam::123456789012:user/test-user"),
        (["arn:aws:iam::123456789012:user/test-user"], ["arn:aws:iam::123456789012:user/test-user"]),
        # ResolvableStrOrList
        ("potato", "potato"),
        (["potato"], ["potato"]),
    ],
)
def test_auxiliar_cast(raw_value, parsed_value):
    assert _Auxiliar.cast(raw_value) == parsed_value
