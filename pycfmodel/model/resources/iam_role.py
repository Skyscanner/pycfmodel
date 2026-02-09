from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.statement_condition import StatementCondition
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import OptionallyNamedPolicyDocument, Resource
from pycfmodel.model.types import Resolvable, ResolvableIntOrStr, ResolvableStr


class IAMRoleProperties(CustomModel):
    """
    Properties:

    - AssumeRolePolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - ManagedPolicyArns: List of ARNs of the IAM managed policies to attach.
    - MaxSessionDuration: Maximum session duration (in seconds).
    - Path: Path to the role.
    - PermissionsBoundary: ARN of the policy used to set the permissions' boundary.
    - Policies: A list of [policy][pycfmodel.model.resources.properties.policy.Policy] objects.
    - RoleName: Name of the role.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html)
    """

    AssumeRolePolicyDocument: Resolvable[PolicyDocument]
    Description: Optional[ResolvableStr] = None
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    MaxSessionDuration: Optional[ResolvableIntOrStr] = None
    Path: Optional[ResolvableStr] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[Resolvable[Policy]]]] = None
    RoleName: Optional[ResolvableStr] = None
    Tags: Optional[Resolvable[List[Tag]]] = None


class IAMRole(Resource):
    """
    Properties:

    - Properties: A [IAM Role properties][pycfmodel.model.resources.iam_role.IAMRoleProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html)
    """

    Type: Literal["AWS::IAM::Role"]
    Properties: Resolvable[IAMRoleProperties]

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        result = []
        policies = self.Properties.Policies if self.Properties and self.Properties.Policies else []
        for policy in policies:
            result.append(OptionallyNamedPolicyDocument(name=policy.PolicyName, policy_document=policy.PolicyDocument))
        return result

    @property
    def assume_role_as_optionally_named_policy_document_list(self) -> List[OptionallyNamedPolicyDocument]:
        return [OptionallyNamedPolicyDocument(name=None, policy_document=self.Properties.AssumeRolePolicyDocument)]

    @property
    def assume_role_statement_conditions(self) -> List[StatementCondition]:
        return [
            statement.Condition
            for statement in self.Properties.AssumeRolePolicyDocument.statement_as_list()
            if statement.Condition
        ]
