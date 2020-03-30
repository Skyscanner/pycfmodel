from typing import ClassVar

from ..types import ResolvableStr, Resolvable
from ..base import CustomModel
from .resource import Resource
from .properties.policy_document import PolicyDocument


class S3BucketPolicyProperties(CustomModel):
    Bucket: ResolvableStr
    PolicyDocument: Resolvable[PolicyDocument]


class S3BucketPolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::S3::BucketPolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[S3BucketPolicyProperties]
