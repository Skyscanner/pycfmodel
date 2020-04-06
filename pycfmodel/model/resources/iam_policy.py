from typing import ClassVar, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.types import ResolvableStrOrList, ResolvableStr, Resolvable


class IAMPolicyProperties(CustomModel):
    """
    Properties:

    - Groups: Friendly name of the IAM groups to attach the policy to.
    - PolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - PolicyName: Name of the policy.
    - Roles: Friendly name of the IAM roles to attach the policy to.
    - Users: Friendly name of the IAM users to attach the policy to.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html)
    """

    Groups: Optional[ResolvableStrOrList] = None
    PolicyDocument: Resolvable[PolicyDocument]
    PolicyName: ResolvableStr
    Roles: Optional[ResolvableStrOrList] = None
    Users: Optional[ResolvableStrOrList] = None


class IAMPolicy(Resource):
    """
    Properties:

    - Properties: A [IAM Policy properties][pycfmodel.model.resources.iam_policy.IAMPolicyProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html)
    """

    TYPE_VALUE: ClassVar = "AWS::IAM::Policy"
    Type: str = TYPE_VALUE
    Properties: Resolvable[IAMPolicyProperties]
