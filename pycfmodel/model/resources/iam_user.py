from typing import Dict, List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.parameter import Parameter
from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


class IAMUserProperties(CustomModel):
    """
    Properties:

    - Groups: List of groups to attach.
    - LoginProfile: Name and password for the user.
    - ManagedPolicyArns: List of ARNs of the IAM managed policies to attach.
    - Path: Path to the user.
    - PermissionsBoundary: ARN of the policy used to set the permissions boundary.
    - Policies: A list of [policy][pycfmodel.model.resources.properties.policy.Policy] objects.
    - UserName: Name of the user.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html)
    """

    Groups: Optional[Resolvable[List[ResolvableStr]]] = None
    LoginProfile: Optional[Dict] = None
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    Path: Optional[ResolvableStr] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[Resolvable[Policy]]]] = None
    UserName: Optional[ResolvableStr] = None


class IAMUser(Resource):
    """
    Properties:

    - Properties: A [IAM User properties][pycfmodel.model.resources.iam_user.IAMUserProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html)
    """

    Type: Literal["AWS::IAM::User"]
    Properties: Optional[Resolvable[IAMUserProperties]] = None

    def has_hardcoded_credentials(self) -> bool:
        """Returns True if login profile password contains a hardcoded string, otherwise False."""
        if self.Properties:
            login_profile = self.Properties.LoginProfile
            if login_profile and login_profile.get("Password"):
                if login_profile["Password"] != Parameter.NO_ECHO_NO_DEFAULT:
                    return True

        return super().has_hardcoded_credentials()

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        result = []
        policies = self.Properties.Policies if self.Properties and self.Properties.Policies else []
        for policy in policies:
            result.append(OptionallyNamedPolicyDocument(policy.PolicyName, policy.PolicyDocument))
        return result
