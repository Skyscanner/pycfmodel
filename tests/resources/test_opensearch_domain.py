import json

import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.opensearch_domain import OpenSearchDomain
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.statement import Principal, Statement
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def valid_empty_opensearch_domain():
    return OpenSearchDomain(**{"Type": "AWS::OpenSearchService::Domain", "Properties": {}})


@pytest.fixture()
def valid_opensearch_domain_from_aws_documentation_examples():
    return OpenSearchDomain(
        **{
            "Type": "AWS::OpenSearchService::Domain",
            "Properties": {
                "AccessPolicies": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::123456789012:user/opensearch-user"},
                            "Action": "es:*",
                            "Resource": "arn:aws:es:us-east-1:123456789012:domain/test/*",
                        }
                    ],
                },
                "AdvancedOptions": {
                    "rest.action.multi.allow_explicit_index": True,
                    "override_main_response_version": True,
                },
                "ClusterConfig": {
                    "DedicatedMasterEnabled": True,
                    "InstanceCount": "2",
                    "ZoneAwarenessEnabled": True,
                    "InstanceType": "m3.medium.search",
                    "DedicatedMasterType": "m3.medium.search",
                    "DedicatedMasterCount": "3",
                },
                "DomainName": "test",
                "EBSOptions": {"EBSEnabled": True, "Iops": "0", "VolumeSize": "20", "VolumeType": "gp2"},
                "EngineVersion": "OpenSearch_1.0",
                "LogPublishingOptions": {
                    "ES_APPLICATION_LOGS": {
                        "CloudWatchLogsLogGroupArn": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearch/domains/opensearch-application-logs",
                        "Enabled": True,
                    },
                    "SEARCH_SLOW_LOGS": {
                        "CloudWatchLogsLogGroupArn": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearch/domains/opensearch-slow-logs",
                        "Enabled": True,
                    },
                    "INDEX_SLOW_LOGS": {
                        "CloudWatchLogsLogGroupArn": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearch/domains/opensearch-index-slow-logs",
                        "Enabled": True,
                    },
                },
            },
        }
    )


@pytest.fixture()
def valid_opensearch_domain_with_access_policies():
    return OpenSearchDomain(
        **{
            "Type": "AWS::OpenSearchService::Domain",
            "Properties": {
                "AccessPolicies": {
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::123456789012:user/opensearch-user"},
                            "Action": "es:*",
                            "Resource": "arn:aws:es:us-east-1:123456789012:domain/test/*",
                        }
                    ]
                }
            },
        }
    )


def test_valid_empty_opensearch_domain_resource_can_be_built(valid_empty_opensearch_domain):
    assert valid_empty_opensearch_domain.Type == "AWS::OpenSearchService::Domain"
    assert valid_empty_opensearch_domain.Properties.AccessPolicies is None
    assert valid_empty_opensearch_domain.Properties.AdvancedOptions is None
    assert valid_empty_opensearch_domain.Properties.AdvancedSecurityOptions is None
    assert valid_empty_opensearch_domain.Properties.ClusterConfig is None
    assert valid_empty_opensearch_domain.Properties.CognitoOptions is None
    assert valid_empty_opensearch_domain.Properties.DomainEndpointOptions is None
    assert valid_empty_opensearch_domain.Properties.DomainName is None
    assert valid_empty_opensearch_domain.Properties.EBSOptions is None
    assert valid_empty_opensearch_domain.Properties.EncryptionAtRestOptions is None
    assert valid_empty_opensearch_domain.Properties.EngineVersion is None
    assert valid_empty_opensearch_domain.Properties.LogPublishingOptions is None
    assert valid_empty_opensearch_domain.Properties.NodeToNodeEncryptionOptions is None
    assert valid_empty_opensearch_domain.Properties.SnapshotOptions is None
    assert valid_empty_opensearch_domain.Properties.Tags is None
    assert valid_empty_opensearch_domain.Properties.VPCOptions is None


def test_valid_opensearch_domain_from_aws_documentation_examples_resource_can_be_built(
    valid_opensearch_domain_from_aws_documentation_examples,
):
    assert valid_opensearch_domain_from_aws_documentation_examples.Type == "AWS::OpenSearchService::Domain"
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Effect == "Allow"
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Action == "es:*"
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Principal.AWS
        == "arn:aws:iam::123456789012:user/opensearch-user"
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Resource
        == "arn:aws:es:us-east-1:123456789012:domain/test/*"
    )
    assert (
        getattr(
            valid_opensearch_domain_from_aws_documentation_examples.Properties.AdvancedOptions,
            "rest.action.multi.allow_explicit_index",
        )
        is True
    )

    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.AdvancedOptions.override_main_response_version
        is True
    )

    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.AdvancedSecurityOptions is None

    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.ClusterConfig.DedicatedMasterEnabled is True
    )
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.ClusterConfig.InstanceCount == 2
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.ClusterConfig.ZoneAwarenessEnabled is True
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.ClusterConfig.InstanceType
        == "m3.medium.search"
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.ClusterConfig.DedicatedMasterType
        == "m3.medium.search"
    )
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.ClusterConfig.DedicatedMasterCount == 3

    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.CognitoOptions is None
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.DomainEndpointOptions is None
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.DomainName == "test"

    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.EBSOptions.EBSEnabled is True
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.EBSOptions.Iops == 0
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.EBSOptions.VolumeSize == 20
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.EBSOptions.VolumeType == "gp2"

    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.EngineVersion == "OpenSearch_1.0"
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.EncryptionAtRestOptions is None

    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.ES_APPLICATION_LOGS.CloudWatchLogsLogGroupArn
        == "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearch/domains/opensearch-application-logs"
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.ES_APPLICATION_LOGS.Enabled
        is True
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.SEARCH_SLOW_LOGS.CloudWatchLogsLogGroupArn
        == "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearch/domains/opensearch-slow-logs"
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.SEARCH_SLOW_LOGS.Enabled
        is True
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.INDEX_SLOW_LOGS.CloudWatchLogsLogGroupArn
        == "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearch/domains/opensearch-index-slow-logs"
    )
    assert (
        valid_opensearch_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.INDEX_SLOW_LOGS.Enabled
        is True
    )

    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.NodeToNodeEncryptionOptions is None
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.SnapshotOptions is None
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.Tags is None
    assert valid_opensearch_domain_from_aws_documentation_examples.Properties.VPCOptions is None


def test_raise_error_if_invalid_fields_in_resource():
    with pytest.raises(ValidationError) as exc_info:
        OpenSearchDomain(**{"Type": "AWS::OpenSearchService::Domain", "Properties": {"DomainName": []}})

    assert json.loads(exc_info.value.json()) == [
        {
            "input": [],
            "loc": ["Properties", "OpenSearchDomainProperties", "DomainName", "str"],
            "msg": "Input should be a valid string",
            "type": "string_type",
            "url": "https://errors.pydantic.dev/2.7/v/string_type",
        },
        {
            "ctx": {"error": "FunctionDict should only have 1 key and be a function"},
            "input": [],
            "loc": ["Properties", "OpenSearchDomainProperties", "DomainName", "FunctionDict"],
            "msg": "Value error, FunctionDict should only have 1 key and be a function",
            "type": "value_error",
            "url": "https://errors.pydantic.dev/2.7/v/value_error",
        },
        {
            "ctx": {"error": "FunctionDict should only have 1 key and be a function"},
            "input": {"DomainName": []},
            "loc": ["Properties", "FunctionDict"],
            "msg": "Value error, FunctionDict should only have 1 key and be a function",
            "type": "value_error",
            "url": "https://errors.pydantic.dev/2.7/v/value_error",
        },
    ]


def test_can_obtain_policy_documents_from_inherited_method(valid_opensearch_domain_with_access_policies):
    assert len(valid_opensearch_domain_with_access_policies.policy_documents) == 1
    assert valid_opensearch_domain_with_access_policies.policy_documents == [
        OptionallyNamedPolicyDocument(
            policy_document=PolicyDocument(
                Statement=[
                    Statement(
                        Effect="Allow",
                        Action="es:*",
                        Resource="arn:aws:es:us-east-1:123456789012:domain/test/*",
                        Principal=Principal(AWS="arn:aws:iam::123456789012:user/opensearch-user"),
                    )
                ]
            ),
            name=None,
        )
    ]
