from typing import ClassVar, List, Optional, Dict

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, ResolvableBool, Resolvable, ResolvableInt


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
