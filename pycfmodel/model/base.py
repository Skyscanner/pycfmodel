from pydantic import BaseModel, ConfigDict, model_validator

from pycfmodel.model.intrinsic_functions import validate_intrinsic_function
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

        # Validate the intrinsic function format
        is_valid, error_message = validate_intrinsic_function(values)
        if not is_valid:
            raise ValueError(f"Invalid intrinsic function: {error_message}")

        return values
