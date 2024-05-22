from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


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
    Policies: Optional[Resolvable[List[Resolvable[Policy]]]] = None


class IAMGroup(Resource):
    """
    Properties:

    - Properties: A [IAM Group properties][pycfmodel.model.resources.iam_group.IAMGroupProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html)
    """

    Type: Literal["AWS::IAM::Group"]
    Properties: Optional[Resolvable[IAMGroupProperties]] = None

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        result = []
        policies = self.Properties.Policies if self.Properties and self.Properties.Policies else []
        for policy in policies:
            result.append(OptionallyNamedPolicyDocument(name=policy.PolicyName, policy_document=policy.PolicyDocument))
        return result
