from typing import ClassVar

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.resources.properties.policy_document import PolicyDocument


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

    TYPE_VALUE: ClassVar = "AWS::S3::BucketPolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[S3BucketPolicyProperties]
