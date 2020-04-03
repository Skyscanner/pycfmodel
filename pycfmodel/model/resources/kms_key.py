from typing import ClassVar, List, Optional, Dict

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, ResolvableBool, Resolvable, ResolvableInt


class KMSKeyProperties(CustomModel):
    """
    Properties:

    - Description:
    - EnableKeyRotation:
    - Enabled:
    - KeyPolicy: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - KeyUsage:
    - PendingWindowInDays:
    - Tags:

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html)
    """

    Description: Optional[ResolvableStr] = None
    EnableKeyRotation: Optional[ResolvableBool] = None
    Enabled: Optional[ResolvableBool] = None
    KeyPolicy: Resolvable[PolicyDocument]
    KeyUsage: Optional[ResolvableStr] = None
    PendingWindowInDays: Optional[ResolvableInt] = None
    Tags: Optional[Resolvable[List[Dict]]] = None


class KMSKey(Resource):
    """
    Properties:

    - Properties: A [KMS Key properties][pycfmodel.model.resources.kms_key.KMSKeyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html)
    """

    TYPE_VALUE: ClassVar = "AWS::KMS::Key"
    Type: str = TYPE_VALUE
    Properties: Resolvable[KMSKeyProperties]
