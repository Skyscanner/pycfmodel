"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import List, Optional, Any, ClassVar

from pydantic import PositiveInt

from .base import CustomModel


class Parameter(CustomModel):
    NO_ECHO_NO_DEFAULT: ClassVar[str] = "NO_ECHO_NO_DEFAULT"
    NO_ECHO_WITH_DEFAULT: ClassVar[str] = "NO_ECHO_WITH_DEFAULT"
    NO_ECHO_WITH_VALUE: ClassVar[str] = "NO_ECHO_WITH_VALUE"
    AllowedPattern: Optional[str] = None
    AllowedValues: Optional[List] = None
    ConstraintDescription: Optional[str] = None
    Default: Optional[Any] = None
    Description: Optional[str] = None
    MaxLength: Optional[PositiveInt] = None
    MaxValue: Optional[PositiveInt] = None
    MinLength: Optional[int] = None
    MinValue: Optional[int] = None
    NoEcho: Optional[bool] = None
    Type: str

    def get_ref_value(self, provided_value=None) -> Optional[str]:
        value = provided_value if provided_value is not None else self.Default
        if self.NoEcho:
            if provided_value is not None:
                return self.NO_ECHO_WITH_VALUE
            elif self.Default:
                return self.NO_ECHO_WITH_DEFAULT
            else:
                return self.NO_ECHO_NO_DEFAULT

        elif self.Type in ["List<Number>", "CommaDelimitedList"]:
            return value.split(",")

        return value if value is None else str(value)
