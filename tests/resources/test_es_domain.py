import json

import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.es_domain import ESDomain


@pytest.fixture()
def valid_empty_es_domain():
    return ESDomain(**{"Type": "AWS::Elasticsearch::Domain", "Properties": {}})


@pytest.fixture()
def valid_es_domain_from_aws_documentation_examples():
    return ESDomain(
        **{
            "Type": "AWS::Elasticsearch::Domain",
            "Properties": {
                "AccessPolicies": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::123456789012:user/es-user"},
                            "Action": "es:*",
                            "Resource": "arn:aws:es:us-east-1:123456789012:domain/test/*",
                        }
                    ],
                },
                "AdvancedOptions": {"rest.action.multi.allow_explicit_index": True},
                "DomainName": "test",
                "EBSOptions": {"EBSEnabled": True, "Iops": "0", "VolumeSize": "20", "VolumeType": "gp2"},
                "ElasticsearchClusterConfig": {
                    "DedicatedMasterEnabled": True,
                    "InstanceCount": "2",
                    "ZoneAwarenessEnabled": True,
                    "InstanceType": "m3.medium.elasticsearch",
                    "DedicatedMasterType": "m3.medium.elasticsearch",
                    "DedicatedMasterCount": "3",
                },
                "ElasticsearchVersion": "7.10",
                "LogPublishingOptions": {
                    "ES_APPLICATION_LOGS": {
                        "CloudWatchLogsLogGroupArn": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearchservice/domains/es-application-logs",
                        "Enabled": True,
                    },
                    "SEARCH_SLOW_LOGS": {
                        "CloudWatchLogsLogGroupArn": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearchservice/domains/es-slow-logs",
                        "Enabled": True,
                    },
                    "INDEX_SLOW_LOGS": {
                        "CloudWatchLogsLogGroupArn": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearchservice/domains/es-index-slow-logs",
                        "Enabled": True,
                    },
                },
            },
        }
    )


def test_valid_empty_es_domain_resource_can_be_built(valid_empty_es_domain):
    assert valid_empty_es_domain.Type == "AWS::Elasticsearch::Domain"
    assert valid_empty_es_domain.Properties.AccessPolicies is None
    assert valid_empty_es_domain.Properties.AdvancedOptions is None
    assert valid_empty_es_domain.Properties.AdvancedSecurityOptions is None
    assert valid_empty_es_domain.Properties.CognitoOptions is None
    assert valid_empty_es_domain.Properties.DomainEndpointOptions is None
    assert valid_empty_es_domain.Properties.DomainName is None
    assert valid_empty_es_domain.Properties.EBSOptions is None
    assert valid_empty_es_domain.Properties.ElasticsearchClusterConfig is None
    assert valid_empty_es_domain.Properties.ElasticsearchVersion is None
    assert valid_empty_es_domain.Properties.EncryptionAtRestOptions is None
    assert valid_empty_es_domain.Properties.LogPublishingOptions is None
    assert valid_empty_es_domain.Properties.NodeToNodeEncryptionOptions is None
    assert valid_empty_es_domain.Properties.SnapshotOptions is None
    assert valid_empty_es_domain.Properties.Tags is None
    assert valid_empty_es_domain.Properties.VPCOptions is None


def test_valid_es_domain_from_aws_documentation_examples_resource_can_be_built(
    valid_es_domain_from_aws_documentation_examples,
):
    assert valid_es_domain_from_aws_documentation_examples.Type == "AWS::Elasticsearch::Domain"
    assert valid_es_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Effect == "Allow"
    assert valid_es_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Action == "es:*"
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Principal.AWS
        == "arn:aws:iam::123456789012:user/es-user"
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.AccessPolicies.Statement[0].Resource
        == "arn:aws:es:us-east-1:123456789012:domain/test/*"
    )

    assert (
        getattr(
            valid_es_domain_from_aws_documentation_examples.Properties.AdvancedOptions,
            "rest.action.multi.allow_explicit_index",
        )
        is True
    )

    assert valid_es_domain_from_aws_documentation_examples.Properties.AdvancedSecurityOptions is None
    assert valid_es_domain_from_aws_documentation_examples.Properties.CognitoOptions is None
    assert valid_es_domain_from_aws_documentation_examples.Properties.DomainEndpointOptions is None
    assert valid_es_domain_from_aws_documentation_examples.Properties.DomainName == "test"
    assert valid_es_domain_from_aws_documentation_examples.Properties.EBSOptions.EBSEnabled is True
    assert valid_es_domain_from_aws_documentation_examples.Properties.EBSOptions.Iops == 0
    assert valid_es_domain_from_aws_documentation_examples.Properties.EBSOptions.VolumeSize == 20
    assert valid_es_domain_from_aws_documentation_examples.Properties.EBSOptions.VolumeType == "gp2"

    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.ElasticsearchClusterConfig.DedicatedMasterEnabled
        is True
    )
    assert valid_es_domain_from_aws_documentation_examples.Properties.ElasticsearchClusterConfig.InstanceCount == 2
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.ElasticsearchClusterConfig.ZoneAwarenessEnabled
        is True
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.ElasticsearchClusterConfig.InstanceType
        == "m3.medium.elasticsearch"
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.ElasticsearchClusterConfig.DedicatedMasterType
        == "m3.medium.elasticsearch"
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.ElasticsearchClusterConfig.DedicatedMasterCount == 3
    )

    assert valid_es_domain_from_aws_documentation_examples.Properties.ElasticsearchVersion == "7.10"
    assert valid_es_domain_from_aws_documentation_examples.Properties.EncryptionAtRestOptions is None

    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.ES_APPLICATION_LOGS.CloudWatchLogsLogGroupArn
        == "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearchservice/domains/es-application-logs"
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.ES_APPLICATION_LOGS.Enabled
        is True
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.SEARCH_SLOW_LOGS.CloudWatchLogsLogGroupArn
        == "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearchservice/domains/es-slow-logs"
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.SEARCH_SLOW_LOGS.Enabled is True
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.INDEX_SLOW_LOGS.CloudWatchLogsLogGroupArn
        == "arn:aws:logs:us-east-1:123456789012:log-group:/aws/opensearchservice/domains/es-index-slow-logs"
    )
    assert (
        valid_es_domain_from_aws_documentation_examples.Properties.LogPublishingOptions.INDEX_SLOW_LOGS.Enabled is True
    )

    assert valid_es_domain_from_aws_documentation_examples.Properties.NodeToNodeEncryptionOptions is None
    assert valid_es_domain_from_aws_documentation_examples.Properties.SnapshotOptions is None
    assert valid_es_domain_from_aws_documentation_examples.Properties.Tags is None
    assert valid_es_domain_from_aws_documentation_examples.Properties.VPCOptions is None


def test_raise_error_if_invalid_fields_in_resource():
    with pytest.raises(ValidationError) as exc_info:
        ESDomain(**{"Type": "AWS::Elasticsearch::Domain", "Properties": {"DomainName": []}})

    assert json.loads(exc_info.value.json()) == [
        {
            "input": [],
            "loc": ["Properties", "ESDomainProperties", "DomainName", "str"],
            "msg": "Input should be a valid string",
            "type": "string_type",
            "url": "https://errors.pydantic.dev/2.7/v/string_type",
        },
        {
            "ctx": {"error": "FunctionDict should only have 1 key and be a function"},
            "input": [],
            "loc": ["Properties", "ESDomainProperties", "DomainName", "FunctionDict"],
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
