from typing import ClassVar, List, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr, ResolvableIntOrStr


class IAMRoleProperties(CustomModel):
    """
    Properties:

    - AssumeRolePolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - ManagedPolicyArns: List of ARNs of the IAM managed policies to attach.
    - MaxSessionDuration: Maximum session duration (in seconds).
    - Path: Path to the role.
    - PermissionsBoundary: ARN of the policy used to set the permissions boundary.
    - Policies: A list of [policy][pycfmodel.model.resources.properties.policy.Policy] objects.
    - RoleName: Name of the role.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html)
    """

    AssumeRolePolicyDocument: Resolvable[PolicyDocument]
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    MaxSessionDuration: Optional[ResolvableIntOrStr] = None
    Path: Optional[ResolvableStr] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[Resolvable[Policy]]]] = None
    RoleName: Optional[ResolvableStr] = None


class IAMRole(Resource):
    """
    Properties:

    - Properties: A [IAM Role properties][pycfmodel.model.resources.iam_role.IAMRoleProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html)
    """

    TYPE_VALUE: ClassVar = "AWS::IAM::Role"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMRoleProperties]
