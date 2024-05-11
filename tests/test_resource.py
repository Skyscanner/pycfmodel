import pytest

from pycfmodel import parse
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.statement import Statement
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.mark.parametrize(
    "template,expected_policy_documents",
    [
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {"NonexistentResource": {"Type": "AWS::Non::Existent", "Properties": {}}},
            },
            [],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {
                    "NonexistentResource": {
                        "Type": "AWS::Non::Existent",
                        "Properties": {"PropertyString": "stringvalue"},
                    }
                },
            },
            [],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {
                    "NonexistentResource": {
                        "Type": "AWS::Non::Existent",
                        "Properties": {
                            "PropertyRandom": "One",
                            "PolicyDocument": {
                                "Statement": [{"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}]
                            },
                        },
                    }
                },
            },
            [
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                )
            ],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {
                    "NonexistentResource": {
                        "Type": "AWS::Non::Existent",
                        "Properties": {
                            "PropertyRandom": "One",
                            "PolicyDocumentOne": {
                                "Statement": [{"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}]
                            },
                            "PolicyDocumentTwo": {
                                "Statement": [{"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}]
                            },
                        },
                    }
                },
            },
            [
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                ),
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                ),
            ],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {
                    "NonexistentResource": {
                        "Type": "AWS::Non::Existent",
                        "Properties": {
                            "PropertyRandom": "One",
                            "PolicyDocumentOne": {
                                "Statement": [{"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}]
                            },
                            "PropertyTwo": {
                                "PolicyDocumentTwo": {
                                    "Statement": [
                                        {"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}
                                    ]
                                }
                            },
                        },
                    }
                },
            },
            [
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                ),
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                ),
            ],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {
                    "NonexistentResource": {
                        "Type": "AWS::Non::Existent",
                        "Properties": {
                            "PropertyRandom": "One",
                            "PropertyOne": {
                                "PolicyDocumentOne": {
                                    "Statement": [
                                        {"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}
                                    ]
                                }
                            },
                            "PropertyTwo": {
                                "PolicyDocumentTwo": {
                                    "Statement": [
                                        {"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}
                                    ]
                                }
                            },
                        },
                    }
                },
            },
            [
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                ),
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                ),
            ],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {
                    "NonexistentResource": {
                        "Type": "AWS::Non::Existent",
                        "Properties": {
                            "PolicyDocumentTwo": [
                                {"Statement": [{"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}]},
                                {
                                    "Statement": [
                                        {"Effect": "Allow", "Action": ["service:GetServiceAnother"], "Resource": "*"}
                                    ]
                                },
                            ]
                        },
                    }
                },
            },
            [
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name=None,
                ),
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetServiceAnother"], Resource="*")]
                    ),
                    name=None,
                ),
            ],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource to Resource class",
                "Resources": {
                    "NonexistentResource": {
                        "Type": "AWS::Non::Existent",
                        "Properties": {
                            "Policies": [
                                {
                                    "PolicyName": "APolicyName",
                                    "PolicyDocument": {
                                        "Statement": [
                                            {"Effect": "Allow", "Action": ["service:GetService"], "Resource": "*"}
                                        ]
                                    },
                                }
                            ]
                        },
                    }
                },
            },
            [
                OptionallyNamedPolicyDocument(
                    policy_document=PolicyDocument(
                        Statement=[Statement(Effect="Allow", Action=["service:GetService"], Resource="*")]
                    ),
                    name="APolicyName",
                )
            ],
        ),
        (
            {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": "Test resolving a nonexistent resource without properties",
                "Resources": {"NonexistentResource": {"Type": "AWS::Non::Existent"}},
            },
            [],
        ),
    ],
)
def test_given_a_template_with_a_resource_it_should_return_its_policy_documents(template, expected_policy_documents):
    resource = parse(template).Resources["NonexistentResource"]
    assert resource.policy_documents == expected_policy_documents
