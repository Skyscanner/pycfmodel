from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr


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
    AdvancedOptions: Optional[ResolvableGeneric] = None
    AdvancedSecurityOptions: Optional[ResolvableGeneric] = None
    CognitoOptions: Optional[ResolvableGeneric] = None
    DomainEndpointOptions: Optional[ResolvableGeneric] = None
    DomainName: Optional[ResolvableStr] = None
    EBSOptions: Optional[ResolvableGeneric] = None
    ElasticsearchClusterConfig: Optional[ResolvableGeneric] = None
    ElasticsearchVersion: Optional[ResolvableStr] = None
    EncryptionAtRestOptions: Optional[ResolvableGeneric] = None
    LogPublishingOptions: Optional[ResolvableGeneric] = None
    NodeToNodeEncryptionOptions: Optional[ResolvableGeneric] = None
    SnapshotOptions: Optional[ResolvableGeneric] = None
    Tags: Optional[Resolvable[List[Tag]]] = None
    VPCOptions: Optional[ResolvableGeneric] = None


class ESDomain(Resource):
    """
    Properties:

    - Properties: An [ESDomainProperties][pycfmodel.model.resources.es_domain.ESDomainProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html)
    """

    Type: Literal["AWS::Elasticsearch::Domain"]
    Properties: Resolvable[ESDomainProperties]
