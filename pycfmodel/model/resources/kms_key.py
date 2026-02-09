from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableStr


class KMSKeyProperties(CustomModel):
    """
    Properties:

    - Description: Description of the CMK.
    - EnableKeyRotation: Enables automatic rotation of the key for the customer master key.
    - Enabled: Specifies whether the customer master key (CMK) is enabled.
    - KeyPolicy: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - KeyUsage: Determines the cryptographic operations.
    - KeySpec: Specifies the type of CMK to create.
    - MultiRegion: Allows multi-Region primary CMK to be replicated in other AWS Regions.
    - PendingWindowInDays: Number of days in the waiting period before AWS KMS deletes a CMK that has been removed from a CloudFormation stack.
    - Tags: Array of key-value pairs.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html)
    """

    BypassPolicyLockoutSafetyCheck: Optional[ResolvableBool] = None
    Description: Optional[ResolvableStr] = None
    Enabled: Optional[ResolvableBool] = None
    EnableKeyRotation: Optional[ResolvableBool] = None
    KeyPolicy: Optional[Resolvable[PolicyDocument]] = None
    KeySpec: Optional[ResolvableStr] = None
    KeyUsage: Optional[ResolvableStr] = None
    MultiRegion: Optional[ResolvableBool] = None
    Origin: Optional[ResolvableStr] = None
    PendingWindowInDays: Optional[ResolvableInt] = None
    Tags: Optional[Resolvable[List[Tag]]] = None


class KMSKey(Resource):
    """
    Properties:

    - Properties: A [KMS Key properties][pycfmodel.model.resources.kms_key.KMSKeyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html)
    """

    Type: Literal["AWS::KMS::Key"]
    Properties: Resolvable[KMSKeyProperties]
