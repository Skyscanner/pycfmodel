from typing import List, Literal

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


class S3BucketPolicyProperties(CustomModel):
    """
    Properties:

    - Bucket: Name of the Amazon S3 bucket to which the policy applies.
    - PolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html)
    """

    Bucket: ResolvableStr
    PolicyDocument: Resolvable[PolicyDocument]


class S3BucketPolicy(Resource):
    """
    Properties:

    - Properties: A [S3 Bucket Policy Properties][pycfmodel.model.resources.s3_bucket_policy.S3BucketPolicyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html)
    """

    Type: Literal["AWS::S3::BucketPolicy"]
    Properties: Resolvable[S3BucketPolicyProperties]

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        return [OptionallyNamedPolicyDocument(name=None, policy_document=self.Properties.PolicyDocument)]
