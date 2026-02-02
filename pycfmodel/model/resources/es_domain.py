from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableModel, ResolvableStr


class ESCognitoOptions(CustomModel):
    """Configures Amazon Cognito authentication for Kibana."""

    Enabled: Optional[ResolvableBool] = None
    IdentityPoolId: Optional[ResolvableStr] = None
    RoleArn: Optional[ResolvableStr] = None
    UserPoolId: Optional[ResolvableStr] = None


ResolvableESCognitoOptions = ResolvableModel(ESCognitoOptions)


class ESDomainEndpointOptions(CustomModel):
    """Specifies additional options for the domain endpoint."""

    CustomEndpoint: Optional[ResolvableStr] = None
    CustomEndpointCertificateArn: Optional[ResolvableStr] = None
    CustomEndpointEnabled: Optional[ResolvableBool] = None
    EnforceHTTPS: Optional[ResolvableBool] = None
    TLSSecurityPolicy: Optional[ResolvableStr] = None


ResolvableESDomainEndpointOptions = ResolvableModel(ESDomainEndpointOptions)


class ESEBSOptions(CustomModel):
    """Amazon EBS volume configurations."""

    EBSEnabled: Optional[ResolvableBool] = None
    Iops: Optional[ResolvableInt] = None
    VolumeSize: Optional[ResolvableInt] = None
    VolumeType: Optional[ResolvableStr] = None


ResolvableESEBSOptions = ResolvableModel(ESEBSOptions)


class ESEncryptionAtRestOptions(CustomModel):
    """Encryption at rest configuration."""

    Enabled: Optional[ResolvableBool] = None
    KmsKeyId: Optional[ResolvableStr] = None


ResolvableESEncryptionAtRestOptions = ResolvableModel(ESEncryptionAtRestOptions)


class ESNodeToNodeEncryptionOptions(CustomModel):
    """Node-to-node encryption configuration."""

    Enabled: Optional[ResolvableBool] = None


ResolvableESNodeToNodeEncryptionOptions = ResolvableModel(ESNodeToNodeEncryptionOptions)


class ESSnapshotOptions(CustomModel):
    """Automated snapshot configuration."""

    AutomatedSnapshotStartHour: Optional[ResolvableInt] = None


ResolvableESSnapshotOptions = ResolvableModel(ESSnapshotOptions)


class ESVPCOptions(CustomModel):
    """VPC configuration."""

    SecurityGroupIds: Optional[Resolvable[List[ResolvableStr]]] = None
    SubnetIds: Optional[Resolvable[List[ResolvableStr]]] = None


ResolvableESVPCOptions = ResolvableModel(ESVPCOptions)


class ESMasterUserOptions(CustomModel):
    """Master user options for fine-grained access control."""

    MasterUserARN: Optional[ResolvableStr] = None
    MasterUserName: Optional[ResolvableStr] = None
    MasterUserPassword: Optional[ResolvableStr] = None


ResolvableESMasterUserOptions = ResolvableModel(ESMasterUserOptions)


class ESAdvancedSecurityOptions(CustomModel):
    """Specifies options for fine-grained access control."""

    Enabled: Optional[ResolvableBool] = None
    InternalUserDatabaseEnabled: Optional[ResolvableBool] = None
    MasterUserOptions: Optional[ResolvableESMasterUserOptions] = None


ResolvableESAdvancedSecurityOptions = ResolvableModel(ESAdvancedSecurityOptions)


class ESZoneAwarenessConfig(CustomModel):
    """Zone awareness configuration."""

    AvailabilityZoneCount: Optional[ResolvableInt] = None


ResolvableESZoneAwarenessConfig = ResolvableModel(ESZoneAwarenessConfig)


class ElasticsearchClusterConfig(CustomModel):
    """Cluster configuration."""

    DedicatedMasterCount: Optional[ResolvableInt] = None
    DedicatedMasterEnabled: Optional[ResolvableBool] = None
    DedicatedMasterType: Optional[ResolvableStr] = None
    InstanceCount: Optional[ResolvableInt] = None
    InstanceType: Optional[ResolvableStr] = None
    WarmCount: Optional[ResolvableInt] = None
    WarmEnabled: Optional[ResolvableBool] = None
    WarmType: Optional[ResolvableStr] = None
    ZoneAwarenessConfig: Optional[ResolvableESZoneAwarenessConfig] = None
    ZoneAwarenessEnabled: Optional[ResolvableBool] = None


ResolvableElasticsearchClusterConfig = ResolvableModel(ElasticsearchClusterConfig)


class ESDomainProperties(CustomModel):
    """
    Properties:

    - AccessPolicies: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - AdvancedOptions: Additional options to specify for the OpenSearch Service domain.
    - AdvancedSecurityOptions: Specifies options for fine-grained access control.
    - CognitoOptions: Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
    - DomainEndpointOptions: Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
    - DomainName: A name for the OpenSearch Service domain.
    - EBSOptions: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.
    - ElasticsearchClusterConfig: ElasticsearchClusterConfig is a property of the AWS::Elasticsearch::Domain resource that configures the cluster of an Amazon OpenSearch Service domain.
    - ElasticsearchVersion: The version of Elasticsearch to use, such as 2.3. If not specified, 1.5 is used as the default.
    - EncryptionAtRestOptions: Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service key to use.
    - LogPublishingOptions: An object with one or more of the following keys: SEARCH_SLOW_LOGS, ES_APPLICATION_LOGS, INDEX_SLOW_LOGS, AUDIT_LOGS, depending on the types of logs you want to publish. Each key needs a valid LogPublishingOption value.
    - NodeToNodeEncryptionOptions: Specifies whether node-to-node encryption is enabled.
    - SnapshotOptions: DEPRECATED. The automated snapshot configuration for the OpenSearch Service domain indices.
    - Tags: An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.
    - VPCOptions: The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html)
    """

    AccessPolicies: Optional[Resolvable[PolicyDocument]] = None
    AdvancedOptions: Optional[Resolvable[dict]] = None
    AdvancedSecurityOptions: Optional[ResolvableESAdvancedSecurityOptions] = None
    CognitoOptions: Optional[ResolvableESCognitoOptions] = None
    DomainEndpointOptions: Optional[ResolvableESDomainEndpointOptions] = None
    DomainName: Optional[ResolvableStr] = None
    EBSOptions: Optional[ResolvableESEBSOptions] = None
    ElasticsearchClusterConfig: Optional[ResolvableElasticsearchClusterConfig] = None
    ElasticsearchVersion: Optional[ResolvableStr] = None
    EncryptionAtRestOptions: Optional[ResolvableESEncryptionAtRestOptions] = None
    LogPublishingOptions: Optional[Resolvable[dict]] = None
    NodeToNodeEncryptionOptions: Optional[ResolvableESNodeToNodeEncryptionOptions] = None
    SnapshotOptions: Optional[ResolvableESSnapshotOptions] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VPCOptions: Optional[ResolvableESVPCOptions] = None


class ESDomain(Resource):
    """
    Properties:

    - Properties: An [ESDomainProperties][pycfmodel.model.resources.es_domain.ESDomainProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html)
    """

    Type: Literal["AWS::Elasticsearch::Domain"]
    Properties: Resolvable[ESDomainProperties]
