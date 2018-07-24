"""
Copyright 2018 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from .statement import Statement


class PolicyDocument(object):

    IAM_ACTIONS = [
        "IAM:ResetServiceSpecificCredential",
        "IAM:UpdateServiceSpecificCredential",
        "IAM:EnableMFADevice",
        "IAM:ListUsers",
        "IAM:CreateServiceLinkedRole",
        "IAM:ListRolePolicies",
        "IAM:PutRolePolicy",
        "IAM:DeleteAccountPasswordPolicy",
        "IAM:ListSSHPublicKeys",
        "IAM:ListAttachedUserPolicies",
        "IAM:AddUserToGroup",
        "IAM:UpdateAssumeRolePolicy",
        "IAM:ListEntitiesForPolicy",
        "IAM:DeleteServiceLinkedRole",
        "IAM:ListServerCertificates",
        "IAM:ListAccountAliases",
        "IAM:PassRole",
        "IAM:GetContextKeysForCustomPolicy",
        "IAM:ListInstanceProfiles",
        "IAM:ListMFADevices",
        "IAM:UploadSigningCertificate",
        "IAM:DeleteRole",
        "IAM:SimulateCustomPolicy",
        "IAM:CreateServiceSpecificCredential",
        "IAM:UpdateRoleDescription",
        "IAM:ResyncMFADevice",
        "IAM:AttachGroupPolicy",
        "IAM:ListAttachedRolePolicies",
        "IAM:ListPoliciesGrantingServiceAccess",
        "IAM:GetInstanceProfile",
        "IAM:UpdateAccessKey",
        "IAM:AddClientIDToOpenIDConnectProvider",
        "IAM:ListGroupPolicies",
        "IAM:DeleteOpenIDConnectProvider",
        "IAM:CreateInstanceProfile",
        "IAM:PutUserPolicy",
        "IAM:ChangePassword",
        "IAM:GenerateServiceLastAccessedDetails"
        "IAM:CreateOpenIDConnectProvider",
        "IAM:GetOpenIDConnectProvider",
        "IAM:DeleteGroup",
        "IAM:DeleteRolePolicy",
        "IAM:ListServiceSpecificCredentials",
        "IAM:ListRoles",
        "IAM:CreateSAMLProvider",
        "IAM:ListPolicyVersions",
        "IAM:DeleteSSHPublicKey",
        "IAM:CreateGroup",
        "IAM:CreateUser",
        "IAM:ListAccessKeys",
        "IAM:UploadServerCertificate",
        "IAM:GetRole",
        "IAM:UploadSSHPublicKey",
        "IAM:RemoveRoleFromInstanceProfile",
        "IAM:UpdateSigningCertificate",
        "IAM:DeleteLoginProfile",
        "IAM:UpdateUser",
        "IAM:ListVirtualMFADevices",
        "IAM:GetSAMLProvider",
        "IAM:AttachRolePolicy",
        "IAM:UpdateAccountPasswordPolicy",
        "IAM:CreatePolicy",
        "IAM:DeleteServiceSpecificCredential",
        "IAM:GetServiceLinkedRoleDeletionStatus",
        "IAM:GetGroupPolicy",
        "IAM:GetServiceLastAccessedDetailsWithEntities",
        "IAM:DetachUserPolicy",
        "IAM:GetLoginProfile",
        "IAM:DeleteUserPolicy",
        "IAM:UpdateLoginProfile",
        "IAM:GetPolicyVersion",
        "IAM:AddRoleToInstanceProfile",
        "IAM:UpdateServerCertificate",
        "IAM:DeactivateMFADevice",
        "IAM:GetAccountPasswordPolicy",
        "IAM:GetUser",
        "IAM:DeleteVirtualMFADevice",
        "IAM:DeletePolicyVersion",
        "IAM:GetServiceLastAccessedDetails",
        "IAM:RemoveUserFromGroup",
        "IAM:AttachUserPolicy",
        "IAM:UpdateOpenIDConnectProviderThumbprint",
        "IAM:GetAccessKeyLastUsed",
        "IAM:DeleteGroupPolicy",
        "IAM:DeleteAccountAlias",
        "IAM:GetGroup",
        "IAM:UpdateSSHPublicKey",
        "IAM:CreateAccessKey",
        "IAM:DetachRolePolicy",
        "IAM:GetSSHPublicKey",
        "IAM:ListAttachedGroupPolicies",
        "IAM:CreateAccountAlias",
        "IAM:DeleteSigningCertificate",
        "IAM:ListGroupsForUser",
        "IAM:ListOpenIDConnectProviders",
        "IAM:UpdateSAMLProvider",
        "IAM:ListInstanceProfilesForRole",
        "IAM:CreateVirtualMFADevice",
        "IAM:ListGroups",
        "IAM:DeleteUser",
        "IAM:GetAccountAuthorizationDetails",
        "IAM:DeletePolicy",
        "IAM:ListSigningCertificates",
        "IAM:PutGroupPolicy",
        "IAM:RemoveClientIDFromOpenIDConnectProvider",
        "IAM:ListPolicies",
        "IAM:GetContextKeysForPrincipalPolicy",
        "IAM:GenerateCredentialReport",
        "IAM:SetDefaultPolicyVersion",
        "IAM:CreateRole",
        "IAM:CreatePolicyVersion",
        "IAM:GetAccountSummary",
        "IAM:GetServerCertificate",
        "IAM:DetachGroupPolicy",
        "IAM:DeleteSAMLProvider",
        "IAM:GetUserPolicy",
        "IAM:GetCredentialReport",
        "IAM:DeleteAccessKey",
        "IAM:DeleteServerCertificate",
        "IAM:ListUserPolicies",
        "IAM:ListSAMLProviders",
        "IAM:GetRolePolicy",
        "IAM:DeleteInstanceProfile",
        "IAM:CreateLoginProfile",
        "IAM:SimulatePrincipalPolicy",
        "IAM:UpdateGroup",
        "IAM:GetPolicy"
    ]

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

    def star_resource_statements(self):
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

    def wildcard_allowed_actions(self, pattern=None):
        """
        Find statements which allow wildcard actions.

        A pattern can be specified for the wildcard action
        """

        wildcard_allowed = []

        for statement in self.statements:
            if statement.wildcard_actions(pattern) and statement.effect == "Allow":
                wildcard_allowed.append(statement)

        return wildcard_allowed

    def wildcard_allowed_principals(self, pattern=None):
        """
        Find statements which allow wildcard principals.

        A pattern can be specified for the wildcard principal
        """

        wildcard_allowed = []

        for statement in self.statements:
            if statement.wildcard_principals(pattern) and statement.effect == "Allow":
                wildcard_allowed.append(statement)

        return wildcard_allowed

    def nonwhitelisted_allowed_principals(self, whitelist=None):
        """Find non whitelisted allowed principals."""

        if not whitelist:
            return []

        nonwhitelisted = []
        for statement in self.statements:
            if statement.non_whitelisted_principals(whitelist) and statement.effect == "Allow":
                nonwhitelisted.append(statement)

        return nonwhitelisted

    def allows_not_principal(self):
        """Find allowed not-principals."""
        not_principals = []
        for statement in self.statements:
            if statement.not_principal and statement.effect == "Allow":
                not_principals.append(statement)

        return not_principals

    def get_iam_actions(self, difference=False):
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
                    actions = [
                        iam for iam in self.IAM_ACTIONS
                        if iam.startswith(action[:wildcard])
                    ]
                elif wildcard == 0:
                    actions = self.IAM_ACTIONS
                elif action in self.IAM_ACTIONS:
                    actions = [action]

                if difference:
                    return list(set(self.IAM_ACTIONS).difference(set(actions)))

        return actions
