from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


class IAMManagedPolicyProperties(CustomModel):
    """
    Properties:

    - Description: Description of the policy.
    - Groups: Friendly name of the IAM groups to attach the policy to.
    - ManagedPolicyName: Name of the policy.
    - Path: Path to the policy.
    - PolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - Roles: Friendly name of the IAM roles to attach the policy to.
    - Users: Friendly name of the IAM users to attach the policy to.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html)
    """

    Description: Optional[ResolvableStr] = None
    Groups: Optional[Resolvable[List[ResolvableStr]]] = None
    ManagedPolicyName: Optional[ResolvableStr] = None
    Path: Optional[ResolvableStr] = None
    PolicyDocument: Resolvable[PolicyDocument]
    Roles: Optional[Resolvable[List[ResolvableStr]]] = None
    Users: Optional[Resolvable[List[ResolvableStr]]] = None


class IAMManagedPolicy(Resource):
    """
    Properties:

    - Properties: A [IAM Managed Policy properties][pycfmodel.model.resources.iam_managed_policy.IAMManagedPolicyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html)
    """

    Type: Literal["AWS::IAM::ManagedPolicy"]
    Properties: Resolvable[IAMManagedPolicyProperties]

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        return [
            OptionallyNamedPolicyDocument(
                name=self.Properties.ManagedPolicyName, policy_document=self.Properties.PolicyDocument
            )
        ]
