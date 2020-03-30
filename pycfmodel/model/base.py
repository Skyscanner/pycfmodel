from pydantic import BaseModel, Extra, root_validator

from pycfmodel.utils import is_resolvable_dict, is_conditional_dict


class CustomModel(BaseModel):
    class Config(BaseModel.Config):
        extra = Extra.forbid

    def dict(self, *args, exclude_unset=True, **kwargs):
        return super().dict(*args, **kwargs, exclude_unset=exclude_unset)


class FunctionDict(BaseModel):
    # Inheriting directly from base model as we want to allow extra fields
    # and there are no default values that we need to suppress
    class Config(BaseModel.Config):
        extra = Extra.allow

    @root_validator(pre=True)
    def check_if_valid_function(cls, values):
        if not is_resolvable_dict(values):
            raise ValueError("FunctionDict should only have 1 key and be a function")
        return values


class ConditionDict(BaseModel):
    # Inheriting directly from base model as we want to allow extra fields
    # and there are no default values that we need to suppress
    class Config(BaseModel.Config):
        extra = Extra.allow

    @root_validator(pre=True)
    def check_if_valid_function(cls, values):
        if not is_conditional_dict(values):
            raise ValueError("ConditionDict should only have 1 key and be a function")
        return values
