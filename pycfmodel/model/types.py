import binascii
from base64 import b64decode
from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network
from typing import Any, List, Type, TypeVar, Union

from pydantic import BeforeValidator, Field, GetCoreSchemaHandler
from pydantic._internal import _schema_generation_shared
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing_extensions import Annotated

from pycfmodel.model.base import FunctionDict


class LooseIPv4Network:
    __slots__ = ()

    def __new__(cls, value: Any) -> IPv4Network:
        return IPv4Network(value, strict=False)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: _schema_generation_shared.GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema = {}
        field_schema.update(type="string", format="looseipv4network")
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: Type[Any],
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def _validate(cls, input_value: Any) -> IPv4Network:
        return cls(input_value)


class LooseIPv6Network:
    __slots__ = ()

    def __new__(cls, value: Any) -> IPv4Network:
        return IPv6Network(value, strict=False)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: _schema_generation_shared.GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema = {}
        field_schema.update(type="string", format="looseipv6network")
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: Type[Any],
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def _validate(cls, input_value: Any) -> IPv6Network:
        return cls(input_value)


class SemiStrictBool:
    __slots__ = ()

    def __new__(cls, value: Any) -> bool:
        """
        Ensure that we only allow bools.
        """
        if isinstance(value, bool):
            return value

        if isinstance(value, str) and value.lower() in ("true", "false"):
            return value.lower() == "true"

        raise ValueError("Value given can't be validated as bool")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: _schema_generation_shared.GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema = {}
        field_schema.update(type="boolean")
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: Type[Any],
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def _validate(cls, input_value: Any) -> bool:
        return cls(input_value)


def validate_binary(value: Any) -> bytearray:
    try:
        value = b64decode(value)
    except binascii.Error:
        raise ValueError("Binary value not valid")
    return value


Binary = Annotated[bytes, BeforeValidator(validate_binary)]


T = TypeVar("T")

Resolvable = Annotated[Union[T, FunctionDict], Field(union_mode="left_to_right")]
InstanceOrListOf = Annotated[Union[T, List[T]], Field(union_mode="left_to_right")]

ResolvableStr = Resolvable[str]
ResolvableArn = ResolvableStr
ResolvableCondition = ResolvableStr
ResolvableInt = Resolvable[int]
ResolvableDate = Resolvable[date]
ResolvableDatetime = Resolvable[datetime]
ResolvableBool = Resolvable[SemiStrictBool]

ResolvableIPv4Network = Resolvable[LooseIPv4Network]
ResolvableIPv6Network = Resolvable[LooseIPv6Network]
ResolvableIPNetwork = Annotated[Union[ResolvableIPv4Network, ResolvableIPv6Network], Field(union_mode="left_to_right")]


ResolvableIntOrStr = Resolvable[Union[int, str]]


ResolvableStrOrList = InstanceOrListOf[ResolvableStr]
ResolvableArnOrList = InstanceOrListOf[ResolvableArn]
ResolvableIntOrList = InstanceOrListOf[ResolvableInt]
ResolvableIPOrList = InstanceOrListOf[ResolvableIPNetwork]
ResolvableBoolOrList = InstanceOrListOf[ResolvableBool]
ResolvableBytesOrList = InstanceOrListOf[Binary]
ResolvableDateOrList = InstanceOrListOf[ResolvableDate]
ResolvableDatetimeOrList = InstanceOrListOf[ResolvableDatetime]
