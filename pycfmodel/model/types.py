import binascii
from base64 import b64decode
from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network
from typing import Any, List, Type, TypeVar, Union

from pydantic import BaseModel, BeforeValidator, Field, GetCoreSchemaHandler
from pydantic._internal import _schema_generation_shared
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing_extensions import Annotated

from pycfmodel.model.base import FunctionDict
from pycfmodel.utils import is_resolvable_dict


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


class _ResolvableModelValidator:
    """
    Validator for ResolvableModel that handles Model | FunctionDict union.

    This bypasses Pydantic's union_mode limitation which cannot be applied
    to model schemas when both types are defined in the same file.
    """

    def __init__(self, model_cls: Type[BaseModel]):
        self.model_cls = model_cls

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        model_cls = self.model_cls

        def validate(value: Any) -> Union[BaseModel, FunctionDict]:
            if isinstance(value, FunctionDict):
                return value
            if isinstance(value, model_cls):
                return value
            if isinstance(value, dict):
                if is_resolvable_dict(value):
                    return FunctionDict.model_validate(value)
                return model_cls.model_validate(value)
            raise ValueError(f"Expected {model_cls.__name__}, FunctionDict, or dict")

        return core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: x.model_dump() if isinstance(x, BaseModel) else x
            ),
        )


def ResolvableModel(model_cls: Type[BaseModel]) -> type:
    """
    Create a resolvable type for a nested Pydantic model.

    This allows fields to accept either a model instance or a CloudFormation
    intrinsic function (like {"Ref": "..."} or {"Fn::Sub": "..."}).

    Unlike the regular Resolvable[T] type, this works with model classes
    defined in the same file, avoiding Pydantic's union_mode limitation.

    Usage:
        class NestedModel(CustomModel):
            field1: ResolvableStr
            field2: ResolvableInt

        # Create the resolvable type alias
        ResolvableNestedModel = ResolvableModel(NestedModel)

        class ParentModel(CustomModel):
            nested: Optional[ResolvableNestedModel] = None  # Use Optional for nullable

    Args:
        model_cls: The Pydantic model class to make resolvable.

    Returns:
        An Annotated type that accepts either the model or a FunctionDict.
    """
    return Annotated[
        Union[model_cls, FunctionDict],
        _ResolvableModelValidator(model_cls),
    ]
