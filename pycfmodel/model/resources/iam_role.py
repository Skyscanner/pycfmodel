from typing import ClassVar, List, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.statement_condition import StatementCondition
from pycfmodel.model.resources.resource import OptionallyNamedPolicyDocument, Resource
from pycfmodel.model.types import Resolvable, ResolvableIntOrStr, ResolvableStr


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

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        result = []
        policies = self.Properties.Policies if self.Properties and self.Properties.Policies else []
        for policy in policies:
            result.append(OptionallyNamedPolicyDocument(name=policy.PolicyName, policy_document=policy.PolicyDocument))
        return result

    @property
    def all_statement_conditions(self) -> List[StatementCondition]:
        assume_role_policy_document_conditions = [
            statement.Condition
            for statement in self.Properties.AssumeRolePolicyDocument.statement_as_list()
            if statement.Condition
        ]
        return super().all_statement_conditions + assume_role_policy_document_conditions
