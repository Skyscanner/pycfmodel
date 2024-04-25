import pytest

from pycfmodel.model.resources.kms_key import KMSKey
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def kms_key():
    return KMSKey(
        **{
            "Type": "AWS::KMS::Key",
            "Properties": {
                "Description": "Symmetric CMK for signing and verification",
                "KeySpec": "SYMMETRIC_DEFAULT",
                "KeyUsage": "SIGN_VERIFY",
                "MultiRegion": True,
                "EnableKeyRotation": True,
                "BypassPolicyLockoutSafetyCheck": False,
                "Origin": "AWS_KMS",
                "KeyPolicy": {
                    "Version": "2012-10-17",
                    "Id": "key-default-1",
                    "Statement": [
                        {
                            "Sid": "Enable IAM User Permissions",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::111122223333:root"},
                            "Action": "kms:*",
                            "Resource": "*",
                        },
                        {
                            "Sid": "Allow administration of the key",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::111122223333:role/Admin"},
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
                        },
                        {
                            "Sid": "Allow use of the key",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::111122223333:role/Developer"},
                            "Action": ["kms:Sign", "kms:Verify", "kms:DescribeKey"],
                            "Resource": "*",
                        },
                    ],
                },
            },
        }
    )


@pytest.fixture()
def kms_key_no_policy():
    return KMSKey(
        **{
            "Type": "AWS::KMS::Key",
            "Properties": {
                "Enabled": True,
                "EnableKeyRotation": True,
            },
        }
    )


def test_actions(kms_key):
    assert [
        "kms:CancelKeyDeletion",
        "kms:ConnectCustomKeyStore",
        "kms:CreateAlias",
        "kms:CreateCustomKeyStore",
        "kms:CreateGrant",
        "kms:CreateKey",
        "kms:Decrypt",
        "kms:DeleteAlias",
        "kms:DeleteCustomKeyStore",
        "kms:DeleteImportedKeyMaterial",
        "kms:DescribeCustomKeyStores",
        "kms:DescribeKey",
        "kms:DisableKey",
        "kms:DisableKeyRotation",
        "kms:DisconnectCustomKeyStore",
        "kms:EnableKey",
        "kms:EnableKeyRotation",
        "kms:Encrypt",
        "kms:GenerateDataKey",
        "kms:GenerateDataKeyPair",
        "kms:GenerateDataKeyPairWithoutPlaintext",
        "kms:GenerateDataKeyWithoutPlaintext",
        "kms:GenerateMac",
        "kms:GenerateRandom",
        "kms:GetKeyPolicy",
        "kms:GetKeyRotationStatus",
        "kms:GetParametersForImport",
        "kms:GetPublicKey",
        "kms:ImportKeyMaterial",
        "kms:ListAliases",
        "kms:ListGrants",
        "kms:ListKeyPolicies",
        "kms:ListKeyRotations",
        "kms:ListKeys",
        "kms:ListResourceTags",
        "kms:ListRetirableGrants",
        "kms:PutKeyPolicy",
        "kms:ReEncryptFrom",
        "kms:ReEncryptTo",
        "kms:ReplicateKey",
        "kms:RetireGrant",
        "kms:RevokeGrant",
        "kms:RotateKeyOnDemand",
        "kms:ScheduleKeyDeletion",
        "kms:Sign",
        "kms:SynchronizeMultiRegionKey",
        "kms:TagResource",
        "kms:UntagResource",
        "kms:UpdateAlias",
        "kms:UpdateCustomKeyStore",
        "kms:UpdateKeyDescription",
        "kms:UpdatePrimaryRegion",
        "kms:Verify",
        "kms:VerifyMac",
    ] == kms_key.Properties.KeyPolicy.get_allowed_actions()


def test_kms_policy_documents(kms_key):
    assert kms_key.policy_documents == [
        OptionallyNamedPolicyDocument(
            name=None,
            policy_document=PolicyDocument(
                **{
                    "Version": "2012-10-17",
                    "Id": "key-default-1",
                    "Statement": [
                        {
                            "Sid": "Enable IAM User Permissions",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::111122223333:root"},
                            "Action": "kms:*",
                            "Resource": "*",
                        },
                        {
                            "Sid": "Allow administration of the key",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::111122223333:role/Admin"},
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
                        },
                        {
                            "Sid": "Allow use of the key",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::111122223333:role/Developer"},
                            "Action": ["kms:Sign", "kms:Verify", "kms:DescribeKey"],
                            "Resource": "*",
                        },
                    ],
                }
            ),
        )
    ]


def test_kms_no_policy(kms_key_no_policy):
    assert kms_key_no_policy.Properties.KeyPolicy is None
