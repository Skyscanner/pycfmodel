from typing import ClassVar, List, Optional, Dict

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, ResolvableBool, Resolvable, ResolvableInt


class KMSKeyProperties(CustomModel):
    """
    Properties:

    - Description: Description of the CMK.
    - EnableKeyRotation: Enables automatic rotation of the key for the customer master key.
    - Enabled: Specifies whether the customer master key (CMK) is enabled.
    - KeyPolicy: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - KeyUsage: Determines the cryptographic operations.
    - PendingWindowInDays: Number of days in the waiting period before AWS KMS deletes a CMK that has been removed from a CloudFormation stack.
    - Tags: Array of key-value pairs.

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
