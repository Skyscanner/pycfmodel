import re
from typing import List, Pattern, Union, Optional

from pydantic import Extra

from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.resources.properties.statement import Statement
from pycfmodel.model.types import Resolvable, ResolvableDate

_IAM_ACTIONS = [
    "IAM:AddClientIDToOpenIDConnectProvider",
    "IAM:AddRoleToInstanceProfile",
    "IAM:AddUserToGroup",
    "IAM:AttachGroupPolicy",
    "IAM:AttachRolePolicy",
    "IAM:AttachUserPolicy",
    "IAM:ChangePassword",
    "IAM:CreateAccessKey",
    "IAM:CreateAccountAlias",
    "IAM:CreateGroup",
    "IAM:CreateInstanceProfile",
    "IAM:CreateLoginProfile",
    "IAM:CreateOpenIDConnectProvider",
    "IAM:CreatePolicy",
    "IAM:CreatePolicyVersion",
    "IAM:CreateRole",
    "IAM:CreateSAMLProvider",
    "IAM:CreateServiceLinkedRole",
    "IAM:CreateServiceSpecificCredential",
    "IAM:CreateUser",
    "IAM:CreateVirtualMFADevice",
    "IAM:DeactivateMFADevice",
    "IAM:DeleteAccessKey",
    "IAM:DeleteAccountAlias",
    "IAM:DeleteAccountPasswordPolicy",
    "IAM:DeleteGroup",
    "IAM:DeleteGroupPolicy",
    "IAM:DeleteInstanceProfile",
    "IAM:DeleteLoginProfile",
    "IAM:DeleteOpenIDConnectProvider",
    "IAM:DeletePolicy",
    "IAM:DeletePolicyVersion",
    "IAM:DeleteRole",
    "IAM:DeleteRolePolicy",
    "IAM:DeleteSAMLProvider",
    "IAM:DeleteServerCertificate",
    "IAM:DeleteServiceLinkedRole",
    "IAM:DeleteServiceSpecificCredential",
    "IAM:DeleteSigningCertificate",
    "IAM:DeleteSSHPublicKey",
    "IAM:DeleteUser",
    "IAM:DeleteUserPolicy",
    "IAM:DeleteVirtualMFADevice",
    "IAM:DetachGroupPolicy",
    "IAM:DetachRolePolicy",
    "IAM:DetachUserPolicy",
    "IAM:EnableMFADevice",
    "IAM:GenerateCredentialReport",
    "IAM:GenerateServiceLastAccessedDetails",
    "IAM:GetAccessKeyLastUsed",
    "IAM:GetAccountAuthorizationDetails",
    "IAM:GetAccountPasswordPolicy",
    "IAM:GetAccountSummary",
    "IAM:GetContextKeysForCustomPolicy",
    "IAM:GetContextKeysForPrincipalPolicy",
    "IAM:GetCredentialReport",
    "IAM:GetGroup",
    "IAM:GetGroupPolicy",
    "IAM:GetInstanceProfile",
    "IAM:GetLoginProfile",
    "IAM:GetOpenIDConnectProvider",
    "IAM:GetPolicy",
    "IAM:GetPolicyVersion",
    "IAM:GetRole",
    "IAM:GetRolePolicy",
    "IAM:GetSAMLProvider",
    "IAM:GetServerCertificate",
    "IAM:GetServiceLastAccessedDetails",
    "IAM:GetServiceLastAccessedDetailsWithEntities",
    "IAM:GetServiceLinkedRoleDeletionStatus",
    "IAM:GetSSHPublicKey",
    "IAM:GetUser",
    "IAM:GetUserPolicy",
    "IAM:ListAccessKeys",
    "IAM:ListAccountAliases",
    "IAM:ListAttachedGroupPolicies",
    "IAM:ListAttachedRolePolicies",
    "IAM:ListAttachedUserPolicies",
    "IAM:ListEntitiesForPolicy",
    "IAM:ListGroupPolicies",
    "IAM:ListGroups",
    "IAM:ListGroupsForUser",
    "IAM:ListInstanceProfiles",
    "IAM:ListInstanceProfilesForRole",
    "IAM:ListMFADevices",
    "IAM:ListOpenIDConnectProviders",
    "IAM:ListPolicies",
    "IAM:ListPoliciesGrantingServiceAccess",
    "IAM:ListPolicyVersions",
    "IAM:ListRolePolicies",
    "IAM:ListRoles",
    "IAM:ListSAMLProviders",
    "IAM:ListServerCertificates",
    "IAM:ListServiceSpecificCredentials",
    "IAM:ListSigningCertificates",
    "IAM:ListSSHPublicKeys",
    "IAM:ListUserPolicies",
    "IAM:ListUsers",
    "IAM:ListVirtualMFADevices",
    "IAM:PassRole",
    "IAM:PutGroupPolicy",
    "IAM:PutRolePolicy",
    "IAM:PutUserPolicy",
    "IAM:RemoveClientIDFromOpenIDConnectProvider",
    "IAM:RemoveRoleFromInstanceProfile",
    "IAM:RemoveUserFromGroup",
    "IAM:ResetServiceSpecificCredential",
    "IAM:ResyncMFADevice",
    "IAM:SetDefaultPolicyVersion",
    "IAM:SimulateCustomPolicy",
    "IAM:SimulatePrincipalPolicy",
    "IAM:UpdateAccessKey",
    "IAM:UpdateAccountPasswordPolicy",
    "IAM:UpdateAssumeRolePolicy",
    "IAM:UpdateGroup",
    "IAM:UpdateLoginProfile",
    "IAM:UpdateOpenIDConnectProviderThumbprint",
    "IAM:UpdateRoleDescription",
    "IAM:UpdateSAMLProvider",
    "IAM:UpdateServerCertificate",
    "IAM:UpdateServiceSpecificCredential",
    "IAM:UpdateSigningCertificate",
    "IAM:UpdateSSHPublicKey",
    "IAM:UpdateUser",
    "IAM:UploadServerCertificate",
    "IAM:UploadSigningCertificate",
    "IAM:UploadSSHPublicKey",
]


class PolicyDocument(Property):
    """
    Contains information about an attached policy.

    Properties:

    - Statement: A [statement][pycfmodel.model.resources.properties.statement.Statement] object.
    - Version
    """

    class Config(Property.Config):
        extra = Extra.allow

    Statement: Resolvable[Union[Statement, List[Resolvable[Statement]]]]
    Version: Optional[ResolvableDate] = None

    def _statement_as_list(self) -> List[Statement]:
        if isinstance(self.Statement, Statement):
            return [self.Statement]
        return self.Statement

    def statements_with(self, pattern: Pattern) -> List[Statement]:
        """
        Finds all statements which have at least one resource with the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of [statements][pycfmodel.model.resources.properties.statement.Statement].
        """
        return [statement for statement in self._statement_as_list() if statement.resources_with(pattern)]

    def allowed_actions_with(self, pattern: Pattern) -> List[Statement]:
        """
        Finds all statements which have at least one action with the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of [statements][pycfmodel.model.resources.properties.statement.Statement].
        """
        return [
            statement
            for statement in self._statement_as_list()
            if statement.actions_with(pattern) and statement.Effect == "Allow"
        ]

    def allowed_principals_with(self, pattern: Pattern) -> List[str]:
        """
        Finds all allowed principals which match the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of principals.
        """
        principals = set()
        for statement in self._statement_as_list():
            if statement.Effect == "Allow":
                principals.update(statement.principals_with(pattern))
        return list(principals)

    def non_whitelisted_allowed_principals(self, whitelist: List[str]) -> List[str]:
        """
        Find non whitelisted allowed principals.

        Arguments:
            whitelist: List of whitelisted principals.

        Returns:
            List of principals.
        """
        principals = set()
        for statement in self._statement_as_list():
            if statement.Effect == "Allow":
                principals.update(statement.non_whitelisted_principals(whitelist))
        return list(principals)

    def get_iam_actions(self, difference=False) -> List[str]:
        """
        Find all IAM Actions which are specified in statements.

        Arguments:
            difference: when True, the behaviour changes to find the difference between all IAM Actions and those specified in the statements of the policy. Default = False.

        Returns:
            List of matching actions.
        """
        actions = set()
        for statement in self._statement_as_list():
            for action in statement.get_action_list():
                if not isinstance(action, str):
                    continue

                pattern = re.compile(f"^{action}$".replace("*", ".*"), re.IGNORECASE)
                for iam in _IAM_ACTIONS:
                    if pattern.match(iam):
                        actions.add(iam)

        if difference:
            return sorted(set(_IAM_ACTIONS).difference(actions))

        return sorted(actions)
