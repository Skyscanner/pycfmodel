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
from typing import Any

from .constants import IMPLEMENTED_FUNCTIONS, CONDITION_FUNCTIONS


def is_resolvable_dict(value: Any) -> bool:
    return isinstance(value, dict) and len(value) == 1 and next(iter(value)) in IMPLEMENTED_FUNCTIONS


def is_conditional_dict(value: Any) -> bool:
    if isinstance(value, dict):
        for func in value.keys():
            if not any(f in func for f in CONDITION_FUNCTIONS):
                return False
        return True
    return False
