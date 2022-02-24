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


class SemiStrictBool(int):
    """
    SemiStrictBool to allow for bools which are not type-coerced.
    """

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="boolean")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> bool:
        """
        Ensure that we only allow bools.
        """
        if isinstance(value, bool):
            return value

        if isinstance(value, str) and value.lower() in ("true", "false"):
            return value.lower() == "true"

        raise ValueError("Value given can't be validated as bool")


T = TypeVar("T")

Resolvable = Union[T, FunctionDict]
InstanceOrListOf = Union[T, List[T]]

ResolvableStr = Resolvable[str]
ResolvableArn = ResolvableStr
ResolvableCondition = ResolvableStr
ResolvableInt = Resolvable[int]
ResolvableDate = Resolvable[date]
ResolvableDatetime = Resolvable[datetime]
ResolvableBool = Resolvable[SemiStrictBool]

ResolvableIPv4Network = Resolvable[LooseIPv4Network]
ResolvableIPv6Network = Resolvable[LooseIPv6Network]

ResolvableIntOrStr = Resolvable[Union[int, str]]


ResolvableStrOrList = InstanceOrListOf[ResolvableStr]
ResolvableArnOrList = InstanceOrListOf[ResolvableArn]
ResolvableIntOrList = InstanceOrListOf[ResolvableInt]
ResolvableIPOrList = InstanceOrListOf[Union[ResolvableIPv4Network, ResolvableIPv6Network]]
ResolvableBoolOrList = InstanceOrListOf[ResolvableBool]
ResolvableBytesOrList = InstanceOrListOf[bytes]
ResolvableDateOrList = InstanceOrListOf[ResolvableDate]
ResolvableDatetimeOrList = InstanceOrListOf[ResolvableDatetime]
