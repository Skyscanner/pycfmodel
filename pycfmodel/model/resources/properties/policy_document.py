"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import List

from .statement import Statement

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


class PolicyDocument:
    def __init__(self, document):
        self.statements = []
        if not document:
            return
        statement = document.get("Statement")
        if isinstance(statement, dict):
            self.statements = [Statement(statement)]
        elif isinstance(statement, list):
            self.statements = [Statement(s) for s in document.get("Statement")]
        else:
            # TODO: raise
            pass

    def star_resource_statements(self) -> List[Statement]:
        """
        Find statements with a resources that is a * or has a * in it.
        """

        star_resources = []
        for statement in self.statements:
            if not statement.resource:
                continue
            if statement.resource == "*" or (isinstance(statement.resource, list) and "*" in statement.resource):
                star_resources.append(statement)
        return star_resources

    def wildcard_allowed_actions(self, pattern=None) -> List[Statement]:
        """
        Find statements which allow wildcard actions.

        A pattern can be specified for the wildcard action
        """

        wildcard_allowed = []

        for statement in self.statements:
            if statement.wildcard_actions(pattern) and statement.effect == "Allow":
                wildcard_allowed.append(statement)

        return wildcard_allowed

    def wildcard_allowed_principals(self, pattern=None) -> List[Statement]:
        """
        Find statements which allow wildcard principals.

        A pattern can be specified for the wildcard principal
        """

        wildcard_allowed = []

        for statement in self.statements:
            if statement.wildcard_principals(pattern) and statement.effect == "Allow":
                wildcard_allowed.append(statement)

        return wildcard_allowed

    def nonwhitelisted_allowed_principals(self, whitelist=None) -> List[Statement]:
        """Find non whitelisted allowed principals."""

        if not whitelist:
            return []

        nonwhitelisted = []
        for statement in self.statements:
            if statement.non_whitelisted_principals(whitelist) and statement.effect == "Allow":
                nonwhitelisted.append(statement)

        return nonwhitelisted

    def allows_not_principal(self) -> List[Statement]:
        """Find allowed not-principals."""
        not_principals = []
        for statement in self.statements:
            if statement.not_principal and statement.effect == "Allow":
                not_principals.append(statement)

        return not_principals

    def get_iam_actions(self, difference=False) -> List[str]:
        actions = []
        for statement in self.statements:
            action_list = statement.action
            if not action_list:
                continue

            for action in action_list:
                if not isinstance(action, str):
                    # TODO: handle dicts
                    continue
                wildcard = action.find("*")

                if wildcard > 0:
                    actions = [iam for iam in _IAM_ACTIONS if action[:wildcard].lower() in iam.lower()]
                elif wildcard == 0:
                    actions = _IAM_ACTIONS
                elif action.lower() in [iam.lower() for iam in _IAM_ACTIONS]:
                    actions.append(action)

                if difference:
                    return list(
                        set([iam.lower() for iam in _IAM_ACTIONS]).difference(set([act.lower() for act in actions]))
                    )

        return actions
