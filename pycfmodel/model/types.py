from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network, _BaseNetwork
from typing import Any, List, Type, TypeVar, Union

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from pycfmodel.model.base import FunctionDict


class LooseIPv4Network(_BaseNetwork):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = {}
        json_schema.update(type="string", format="looseipv4network")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, __input_value: Any) -> IPv4Network:
        return IPv4Network(__input_value, False)


class LooseIPv6Network(_BaseNetwork):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = {}
        json_schema.update(type="string", format="looseipv6network")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, __input_value: Any) -> IPv6Network:
        return IPv6Network(__input_value, False)


class SemiStrictBool(int):
    """
    SemiStrictBool to allow for bools which are not type-coerced.
    """

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = {}
        json_schema.update(type="boolean")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, __input_value: Any) -> bool:
        """
        Ensure that we only allow bools.
        """
        if isinstance(__input_value, bool):
            return __input_value

        if isinstance(__input_value, str) and __input_value.lower() in ("true", "false"):
            return __input_value.lower() == "true"

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
