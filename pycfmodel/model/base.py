from pydantic import BaseModel, ConfigDict, model_validator

from pycfmodel.utils import is_resolvable_dict


class CustomModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class FunctionDict(BaseModel):
    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    @classmethod
    def check_if_valid_function(cls, values):
        if not is_resolvable_dict(values):
            raise ValueError("FunctionDict should only have 1 key and be a function")
        return values
