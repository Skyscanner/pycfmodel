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
