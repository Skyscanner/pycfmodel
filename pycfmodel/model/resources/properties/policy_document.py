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
        "iam:ResetServiceSpecificCredential",
        "iam:UpdateServiceSpecificCredential",
        "iam:EnableMFADevice",
        "iam:ListUsers",
        "iam:CreateServiceLinkedRole",
        "iam:ListRolePolicies",
        "iam:PutRolePolicy",
        "iam:DeleteAccountPasswordPolicy",
        "iam:ListSSHPublicKeys",
        "iam:ListAttachedUserPolicies",
        "iam:AddUserToGroup",
        "iam:UpdateAssumeRolePolicy",
        "iam:ListEntitiesForPolicy",
        "iam:DeleteServiceLinkedRole",
        "iam:ListServerCertificates",
        "iam:ListAccountAliases",
        "iam:PassRole",
        "iam:GetContextKeysForCustomPolicy",
        "iam:ListInstanceProfiles",
        "iam:ListMFADevices",
        "iam:UploadSigningCertificate",
        "iam:DeleteRole",
        "iam:SimulateCustomPolicy",
        "iam:CreateServiceSpecificCredential",
        "iam:UpdateRoleDescription",
        "iam:ResyncMFADevice",
        "iam:AttachGroupPolicy",
        "iam:ListAttachedRolePolicies",
        "iam:ListPoliciesGrantingServiceAccess",
        "iam:GetInstanceProfile",
        "iam:UpdateAccessKey",
        "iam:AddClientIDToOpenIDConnectProvider",
        "iam:ListGroupPolicies",
        "iam:DeleteOpenIDConnectProvider",
        "iam:CreateInstanceProfile",
        "iam:PutUserPolicy",
        "iam:ChangePassword",
        "iam:GenerateServiceLastAccessedDetails"
        "iam:CreateOpenIDConnectProvider",
        "iam:GetOpenIDConnectProvider",
        "iam:DeleteGroup",
        "iam:DeleteRolePolicy",
        "iam:ListServiceSpecificCredentials",
        "iam:ListRoles",
        "iam:CreateSAMLProvider",
        "iam:ListPolicyVersions",
        "iam:DeleteSSHPublicKey",
        "iam:CreateGroup",
        "iam:CreateUser",
        "iam:ListAccessKeys",
        "iam:UploadServerCertificate",
        "iam:GetRole",
        "iam:UploadSSHPublicKey",
        "iam:RemoveRoleFromInstanceProfile",
        "iam:UpdateSigningCertificate",
        "iam:DeleteLoginProfile",
        "iam:UpdateUser",
        "iam:ListVirtualMFADevices",
        "iam:GetSAMLProvider",
        "iam:AttachRolePolicy",
        "iam:UpdateAccountPasswordPolicy",
        "iam:CreatePolicy",
        "iam:DeleteServiceSpecificCredential",
        "iam:GetServiceLinkedRoleDeletionStatus",
        "iam:GetGroupPolicy",
        "iam:GetServiceLastAccessedDetailsWithEntities",
        "iam:DetachUserPolicy",
        "iam:GetLoginProfile",
        "iam:DeleteUserPolicy",
        "iam:UpdateLoginProfile",
        "iam:GetPolicyVersion",
        "iam:AddRoleToInstanceProfile",
        "iam:UpdateServerCertificate",
        "iam:DeactivateMFADevice",
        "iam:GetAccountPasswordPolicy",
        "iam:GetUser",
        "iam:DeleteVirtualMFADevice",
        "iam:DeletePolicyVersion",
        "iam:GetServiceLastAccessedDetails",
        "iam:RemoveUserFromGroup",
        "iam:AttachUserPolicy",
        "iam:UpdateOpenIDConnectProviderThumbprint",
        "iam:GetAccessKeyLastUsed",
        "iam:DeleteGroupPolicy",
        "iam:DeleteAccountAlias",
        "iam:GetGroup",
        "iam:UpdateSSHPublicKey",
        "iam:CreateAccessKey",
        "iam:DetachRolePolicy",
        "iam:GetSSHPublicKey",
        "iam:ListAttachedGroupPolicies",
        "iam:CreateAccountAlias",
        "iam:DeleteSigningCertificate",
        "iam:ListGroupsForUser",
        "iam:ListOpenIDConnectProviders",
        "iam:UpdateSAMLProvider",
        "iam:ListInstanceProfilesForRole",
        "iam:CreateVirtualMFADevice",
        "iam:ListGroups",
        "iam:DeleteUser",
        "iam:GetAccountAuthorizationDetails",
        "iam:DeletePolicy",
        "iam:ListSigningCertificates",
        "iam:PutGroupPolicy",
        "iam:RemoveClientIDFromOpenIDConnectProvider",
        "iam:ListPolicies",
        "iam:GetContextKeysForPrincipalPolicy",
        "iam:GenerateCredentialReport",
        "iam:SetDefaultPolicyVersion",
        "iam:CreateRole",
        "iam:CreatePolicyVersion",
        "iam:GetAccountSummary",
        "iam:GetServerCertificate",
        "iam:DetachGroupPolicy",
        "iam:DeleteSAMLProvider",
        "iam:GetUserPolicy",
        "iam:GetCredentialReport",
        "iam:DeleteAccessKey",
        "iam:DeleteServerCertificate",
        "iam:ListUserPolicies",
        "iam:ListSAMLProviders",
        "iam:GetRolePolicy",
        "iam:DeleteInstanceProfile",
        "iam:CreateLoginProfile",
        "iam:SimulatePrincipalPolicy",
        "iam:UpdateGroup",
        "iam:GetPolicy"
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
