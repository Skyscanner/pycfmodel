from typing import ClassVar, List, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.iam_policy import IAMPolicy
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import ResolvableStr, Resolvable


class IAMGroupProperties(CustomModel):
    """
    Properties:

    - GroupName: Name of the group.
    - ManagedPolicyArns: ARN of the IAM policies to attach.
    - Path: Path to the group. See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html).
    - Policies: Inline policies embedded in the IAM group.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html)
    """

    GroupName: Optional[ResolvableStr] = None
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    Path: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[IAMPolicy]]] = None


class IAMGroup(Resource):
    """
    Properties:

    - Properties: A [IAM Group properties][pycfmodel.model.resources.iam_group.IAMGroupProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html)
    """

    TYPE_VALUE: ClassVar = "AWS::IAM::Group"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMGroupProperties]
