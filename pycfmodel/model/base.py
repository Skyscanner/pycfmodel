from pydantic import BaseModel, ConfigDict, Extra, model_validator

from pycfmodel.utils import is_resolvable_dict


class CustomModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def dict(self, *args, exclude_unset=True, **kwargs):
        return super().dict(*args, **kwargs, exclude_unset=exclude_unset)


class FunctionDict(BaseModel):
    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    @classmethod
    def check_if_valid_function(cls, values):
        if not is_resolvable_dict(values):
            raise ValueError("FunctionDict should only have 1 key and be a function")
        return values
