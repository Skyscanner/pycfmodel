from contextlib import suppress
from typing import Union

from pydantic import BaseModel, Extra, ValidationError, root_validator

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


class _Auxiliar(BaseModel):
    aux: Union[
        FunctionDict,
        Properties,
        ResolvableBoolOrList,
        ResolvableIntOrList,
        ResolvableDatetimeOrList,
        ResolvableDateOrList,
        ResolvableIPOrList,
        ResolvableArnOrList,
        ResolvableStrOrList,
    ]

    class Config(BaseModel.Config):
        smart_union = True

    @classmethod
    def cast(cls, value):
        with suppress(ValidationError):
            value = _Auxiliar(aux=value).aux

        if isinstance(value, list):
            auxiliar_list = []
            for v in value:
                v = _Auxiliar.cast(v)
                if isinstance(v, dict):
                    v = Generic.parse_obj(v)
                auxiliar_list.append(v)
            value = auxiliar_list

        if isinstance(value, dict):
            value = Generic.parse_obj(value)

        return value


class Generic(BaseModel):
    """Any property under this class will be cast to an existing model of `pycfmodel` if possible."""

    class Config(BaseModel.Config):
        extra = Extra.allow

    @root_validator(pre=True)
    def casting(cls, values):
        return {k: _Auxiliar.cast(v) for k, v in values.items()}


ResolvableGeneric = Resolvable[Generic]
ResolvableGenericOrList = InstanceOrListOf[ResolvableGeneric]
