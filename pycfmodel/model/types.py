from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network, _BaseNetwork
from typing import Any, Dict, Generator, List, TypeVar, Union

from pydantic.networks import NetworkType
from pydantic.typing import AnyCallable

from pycfmodel.model.base import FunctionDict


class LooseIPv4Network(_BaseNetwork):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="string", format="looseipv4network")

    @classmethod
    def __get_validators__(cls) -> Generator[AnyCallable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: NetworkType) -> IPv4Network:
        return IPv4Network(value, False)


class LooseIPv6Network(_BaseNetwork):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="string", format="looseipv6network")

    @classmethod
    def __get_validators__(cls) -> Generator[AnyCallable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: NetworkType) -> IPv6Network:
        return IPv6Network(value, False)


T = TypeVar("T")

Resolvable = Union[T, FunctionDict]
InstanceOrListOf = Union[T, List[T]]

ResolvableStr = Resolvable[str]
ResolvableArn = ResolvableStr
ResolvableCondition = ResolvableStr
ResolvableInt = Resolvable[int]
ResolvableDate = Resolvable[date]
ResolvableDatetime = Resolvable[datetime]
ResolvableBool = Resolvable[bool]
ResolvableDict = Resolvable[dict]

ResolvableIPv4Network = Resolvable[LooseIPv4Network]
ResolvableIPv6Network = Resolvable[LooseIPv6Network]

ResolvableIntOrStr = Resolvable[Union[int, str]]


ResolvableStrOrList = InstanceOrListOf[ResolvableStr]
ResolvableArnOrList = InstanceOrListOf[ResolvableArn]
ResolvableIntOrList = InstanceOrListOf[ResolvableInt]
ResolvableIPOrList = InstanceOrListOf[Union[ResolvableIPv4Network, ResolvableIPv6Network]]
ResolvableBoolOrList = InstanceOrListOf[ResolvableBool]
ResolvableDictOrList = InstanceOrListOf[ResolvableDict]
ResolvableBytesOrList = InstanceOrListOf[bytes]
ResolvableDatetimeOrList = InstanceOrListOf[ResolvableDatetime]
