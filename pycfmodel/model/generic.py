import json
from contextlib import suppress
from typing import Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator
from typing_extensions import Annotated

from pycfmodel.model.base import FunctionDict
from pycfmodel.model.resources.properties.types import Properties
from pycfmodel.model.types import (
    InstanceOrListOf,
    Resolvable,
    ResolvableArnOrList,
    ResolvableBoolOrList,
    ResolvableDateOrList,
    ResolvableDatetimeOrList,
    ResolvableIntOrList,
    ResolvableIPOrList,
    ResolvableStrOrList,
)

AuxType = Annotated[
    Union[
        FunctionDict,
        Properties,
        ResolvableBoolOrList,
        ResolvableIntOrList,
        ResolvableDateOrList,
        ResolvableDatetimeOrList,  # Date can be parsed as Datetime in pydantic v2 so should be ordered accordingly
        ResolvableIPOrList,
        ResolvableArnOrList,
        ResolvableStrOrList,
    ],
    Field(union_mode="left_to_right"),
]


class _Auxiliar(BaseModel):
    aux: AuxType

    @field_validator("aux", mode="before")
    @classmethod
    def validate_string_property_formatted_as_json(cls, value):
        """
        We have detected some properties that are defined as String in CloudFormation but including a
        PolicyDocument in them, such as:
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policydocument
        For that, we try to parse them to a JSON to be evaluated then to a known property.
        If we fail to parse it, it means the property is a String without a JSON in it, we return the property as it is.
        """
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return value
        return value

    @classmethod
    def cast(cls, value):
        with suppress(ValidationError):
            value = _Auxiliar(aux=value).aux

        if isinstance(value, list):
            auxiliar_list = []
            for v in value:
                v = _Auxiliar.cast(v)
                if isinstance(v, dict):
                    v = Generic.model_validate(v)
                auxiliar_list.append(v)
            value = auxiliar_list

        if isinstance(value, dict):
            value = Generic.model_validate(value)

        return value


class Generic(BaseModel):
    """Any property under this class will be cast to an existing model of `pycfmodel` if possible."""

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    @classmethod
    def casting(cls, values):
        if isinstance(values, dict):
            return {k: _Auxiliar.cast(v) for k, v in values.items()}
        raise ValueError(f"Not supported type: {type(values)}")


ResolvableGeneric = Resolvable[Generic]
ResolvableGenericOrList = InstanceOrListOf[ResolvableGeneric]
