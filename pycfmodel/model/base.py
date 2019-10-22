"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from pydantic import BaseModel, Extra, root_validator

from pycfmodel.utils import is_resolvable_dict


class CustomModel(BaseModel):
    class Config(BaseModel.Config):
        extra = Extra.forbid

    def dict(self, *args, skip_defaults=True, **kwargs):
        return super().dict(*args, **kwargs, skip_defaults=skip_defaults)


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
