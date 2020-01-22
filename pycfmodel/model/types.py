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
from datetime import date
from typing import Union, List, TypeVar

from .base import FunctionDict, ConditionDict

T = TypeVar("T")
Resolvable = Union[T, FunctionDict]

ResolvableStr = Resolvable[str]
ResolvableInt = Resolvable[int]
ResolvableDate = Resolvable[date]
ResolvableBool = Resolvable[bool]
ResolvableStrOrList = Resolvable[Union[str, List]]
ResolvableIntOrStr = Resolvable[Union[int, str]]

ResolvableCondition = Union[ConditionDict, ResolvableStr]
