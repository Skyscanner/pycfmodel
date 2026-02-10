from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableModel, ResolvableStr


class CognitoOptions(CustomModel):
    """Configures Amazon Cognito authentication for OpenSearch Dashboards."""

    Enabled: Optional[ResolvableBool] = None
    IdentityPoolId: Optional[ResolvableStr] = None
    RoleArn: Optional[ResolvableStr] = None
    UserPoolId: Optional[ResolvableStr] = None


ResolvableCognitoOptions = ResolvableModel(CognitoOptions)


class DomainEndpointOptions(CustomModel):
    """Specifies additional options for the domain endpoint."""

    CustomEndpoint: Optional[ResolvableStr] = None
    CustomEndpointCertificateArn: Optional[ResolvableStr] = None
    CustomEndpointEnabled: Optional[ResolvableBool] = None
    EnforceHTTPS: Optional[ResolvableBool] = None
    TLSSecurityPolicy: Optional[ResolvableStr] = None


ResolvableDomainEndpointOptions = ResolvableModel(DomainEndpointOptions)


class EBSOptions(CustomModel):
    """Amazon EBS volume configurations."""

    EBSEnabled: Optional[ResolvableBool] = None
    Iops: Optional[ResolvableInt] = None
    Throughput: Optional[ResolvableInt] = None
    VolumeSize: Optional[ResolvableInt] = None
    VolumeType: Optional[ResolvableStr] = None


ResolvableEBSOptions = ResolvableModel(EBSOptions)


class EncryptionAtRestOptions(CustomModel):
    """Encryption at rest configuration."""

    Enabled: Optional[ResolvableBool] = None
    KmsKeyId: Optional[ResolvableStr] = None


ResolvableEncryptionAtRestOptions = ResolvableModel(EncryptionAtRestOptions)


class NodeToNodeEncryptionOptions(CustomModel):
    """Node-to-node encryption configuration."""

    Enabled: Optional[ResolvableBool] = None


ResolvableNodeToNodeEncryptionOptions = ResolvableModel(NodeToNodeEncryptionOptions)


class SnapshotOptions(CustomModel):
    """Automated snapshot configuration."""

    AutomatedSnapshotStartHour: Optional[ResolvableInt] = None


ResolvableSnapshotOptions = ResolvableModel(SnapshotOptions)


class SoftwareUpdateOptions(CustomModel):
    """Software update options."""

    AutoSoftwareUpdateEnabled: Optional[ResolvableBool] = None


ResolvableSoftwareUpdateOptions = ResolvableModel(SoftwareUpdateOptions)


class VPCOptions(CustomModel):
    """VPC configuration."""

    SecurityGroupIds: Optional[Resolvable[List[ResolvableStr]]] = None
    SubnetIds: Optional[Resolvable[List[ResolvableStr]]] = None


ResolvableVPCOptions = ResolvableModel(VPCOptions)


class MasterUserOptions(CustomModel):
    """Master user options for fine-grained access control."""

    MasterUserARN: Optional[ResolvableStr] = None
    MasterUserName: Optional[ResolvableStr] = None
    MasterUserPassword: Optional[ResolvableStr] = None


ResolvableMasterUserOptions = ResolvableModel(MasterUserOptions)


class AdvancedSecurityOptions(CustomModel):
    """Specifies options for fine-grained access control."""

    Enabled: Optional[ResolvableBool] = None
    InternalUserDatabaseEnabled: Optional[ResolvableBool] = None
    MasterUserOptions: Optional[ResolvableMasterUserOptions] = None


ResolvableAdvancedSecurityOptions = ResolvableModel(AdvancedSecurityOptions)


class ZoneAwarenessConfig(CustomModel):
    """Zone awareness configuration."""

    AvailabilityZoneCount: Optional[ResolvableInt] = None


ResolvableZoneAwarenessConfig = ResolvableModel(ZoneAwarenessConfig)


class ClusterConfig(CustomModel):
    """Cluster configuration."""

    DedicatedMasterCount: Optional[ResolvableInt] = None
    DedicatedMasterEnabled: Optional[ResolvableBool] = None
    DedicatedMasterType: Optional[ResolvableStr] = None
    InstanceCount: Optional[ResolvableInt] = None
    InstanceType: Optional[ResolvableStr] = None
    WarmCount: Optional[ResolvableInt] = None
    WarmEnabled: Optional[ResolvableBool] = None
    WarmType: Optional[ResolvableStr] = None
    ZoneAwarenessConfig: Optional[ResolvableZoneAwarenessConfig] = None
    ZoneAwarenessEnabled: Optional[ResolvableBool] = None


ResolvableClusterConfig = ResolvableModel(ClusterConfig)


class OpenSearchDomainProperties(CustomModel):
    """
    Properties:

    - AccessPolicies: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - AdvancedOptions: Additional options to specify for the OpenSearch Service domain.
    - AdvancedSecurityOptions: Specifies options for fine-grained access control.
    - AIMLOptions: Machine learning options for the domain.
    - ClusterConfig: ClusterConfig is a property of the AWS::OpenSearchService::Domain resource that configures an Amazon OpenSearch Service cluster.
    - CognitoOptions: Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
    - DomainEndpointOptions: Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
    - DomainName: A name for the OpenSearch Service domain.
    - EBSOptions: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.
    - EncryptionAtRestOptions: Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service key to use.
    - EngineVersion: The version of OpenSearch to use. The value must be in the format OpenSearch_X.Y or Elasticsearch_X.Y. If not specified, the latest version of OpenSearch is used.
    - IdentityCenterOptions: Identity Center options for the domain.
    - IPAddressType: The IP address type for the domain.
    - LogPublishingOptions: An object with one or more of the following keys: SEARCH_SLOW_LOGS, ES_APPLICATION_LOGS, INDEX_SLOW_LOGS, AUDIT_LOGS, depending on the types of logs you want to publish. Each key needs a valid LogPublishingOption value.
    - NodeToNodeEncryptionOptions: Specifies whether node-to-node encryption is enabled.
    - OffPeakWindowOptions: Off-peak window options for the domain.
    - SkipShardMigrationWait: Whether to skip the shard migration wait.
    - SnapshotOptions: DEPRECATED. The automated snapshot configuration for the OpenSearch Service domain indices.
    - SoftwareUpdateOptions: Software update options for the domain.
    - Tags: An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.
    - VPCOptions: The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html)
    """

    AccessPolicies: Optional[Resolvable[PolicyDocument]] = None
    AdvancedOptions: Optional[Resolvable[dict]] = None
    AdvancedSecurityOptions: Optional[ResolvableAdvancedSecurityOptions] = None
    AIMLOptions: Optional[Resolvable[dict]] = None
    ClusterConfig: Optional[ResolvableClusterConfig] = None
    CognitoOptions: Optional[ResolvableCognitoOptions] = None
    DomainEndpointOptions: Optional[ResolvableDomainEndpointOptions] = None
    DomainName: Optional[ResolvableStr] = None
    EBSOptions: Optional[ResolvableEBSOptions] = None
    EncryptionAtRestOptions: Optional[ResolvableEncryptionAtRestOptions] = None
    EngineVersion: Optional[ResolvableStr] = None
    IdentityCenterOptions: Optional[Resolvable[dict]] = None
    IPAddressType: Optional[ResolvableStr] = None
    LogPublishingOptions: Optional[Resolvable[dict]] = None
    NodeToNodeEncryptionOptions: Optional[ResolvableNodeToNodeEncryptionOptions] = None
    OffPeakWindowOptions: Optional[Resolvable[dict]] = None
    SkipShardMigrationWait: Optional[ResolvableBool] = None
    SnapshotOptions: Optional[ResolvableSnapshotOptions] = None
    SoftwareUpdateOptions: Optional[ResolvableSoftwareUpdateOptions] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VPCOptions: Optional[ResolvableVPCOptions] = None


class OpenSearchDomain(Resource):
    """
    Properties:

    - Properties: An [OpenSearchDomainProperties][pycfmodel.model.resources.opensearch_domain.OpenSearchDomainProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html)
    """

    Type: Literal["AWS::OpenSearchService::Domain"]
    Properties: Resolvable[OpenSearchDomainProperties]
