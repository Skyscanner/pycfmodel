import pytest

from pycfmodel.model.resources.kms_key import KMSKey


@pytest.fixture()
def kms_key():
    return KMSKey(
        **{
            "Type": "AWS::KMS::Key",
            "Properties": {
                "Description": "Test key to test KMS best practices",
                "Enabled": True,
                "EnableKeyRotation": True,
                "KeyPolicy": {
                    "Version": "2012-10-17",
                    "Id": "test_key_policy",
                    "Statement": [
                        {
                            "Sid": "Allow administration of the key",
                            "Effect": "Allow",
                            "Principal": {"AWS": [{"Ref": "Principal"}]},
                            "Action": [
                                "kms:Create*",
                                "kms:Describe*",
                                "kms:Enable*",
                                "kms:List*",
                                "kms:Put*",
                                "kms:Update*",
                                "kms:Revoke*",
                                "kms:Disable*",
                                "kms:Get*",
                                "kms:Delete*",
                                "kms:ScheduleKeyDeletion",
                                "kms:CancelKeyDeletion",
                            ],
                            "Resource": "*",
                        }
                    ],
                },
            },
        }
    )


def test_actions(kms_key):
    assert [
        "kms:CancelKeyDeletion",
        "kms:CreateAlias",
        "kms:CreateCustomKeyStore",
        "kms:CreateGrant",
        "kms:CreateKey",
        "kms:DeleteAlias",
        "kms:DeleteCustomKeyStore",
        "kms:DeleteImportedKeyMaterial",
        "kms:DescribeCustomKeyStores",
        "kms:DescribeKey",
        "kms:DisableKey",
        "kms:DisableKeyRotation",
        "kms:EnableKey",
        "kms:EnableKeyRotation",
        "kms:GetKeyPolicy",
        "kms:GetKeyRotationStatus",
        "kms:GetParametersForImport",
        "kms:GetPublicKey",
        "kms:ListAliases",
        "kms:ListGrants",
        "kms:ListKeyPolicies",
        "kms:ListKeys",
        "kms:ListResourceTags",
        "kms:ListRetirableGrants",
        "kms:PutKeyPolicy",
        "kms:RevokeGrant",
        "kms:ScheduleKeyDeletion",
        "kms:UpdateAlias",
        "kms:UpdateCustomKeyStore",
        "kms:UpdateKeyDescription",
        "kms:UpdatePrimaryRegion",
    ] == kms_key.Properties.KeyPolicy.get_allowed_actions()


def test_kms_policy_documents(kms_key):
    assert kms_key.policy_documents == []
