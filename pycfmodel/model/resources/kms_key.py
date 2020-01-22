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
from typing import ClassVar, List, Optional, Dict

from ..base import CustomModel
from ..types import ResolvableStr, ResolvableInt, ResolvableBool, Resolvable
from .properties.policy_document import PolicyDocument
from .resource import Resource


class KMSKeyProperties(CustomModel):
    Description: Optional[ResolvableStr] = None
    EnableKeyRotation: Optional[ResolvableBool] = None
    Enabled: Optional[ResolvableBool] = None
    KeyPolicy: Resolvable[PolicyDocument]
    KeyUsage: Optional[ResolvableStr] = None
    PendingWindowInDays: Optional[ResolvableInt] = None
    Tags: Optional[Resolvable[List[Dict]]] = None


class KMSKey(Resource):
    TYPE_VALUE: ClassVar = "AWS::KMS::Key"
    Type: str = TYPE_VALUE
    Properties: Resolvable[KMSKeyProperties]
