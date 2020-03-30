from typing import ClassVar

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.resources.properties.policy_document import PolicyDocument


class S3BucketPolicyProperties(CustomModel):
    Bucket: ResolvableStr
    PolicyDocument: Resolvable[PolicyDocument]


class S3BucketPolicy(Resource):
    TYPE_VALUE: ClassVar = "AWS::S3::BucketPolicy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[S3BucketPolicyProperties]
