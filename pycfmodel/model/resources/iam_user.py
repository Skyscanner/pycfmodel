from typing import ClassVar, List, Optional, Dict

from ..parameter import Parameter
from ..types import ResolvableStr, Resolvable
from ..base import CustomModel
from .properties.policy import Policy
from .resource import Resource


class IAMUserProperties(CustomModel):
    Groups: Optional[Resolvable[List[ResolvableStr]]] = None
    LoginProfile: Optional[Dict] = None
    ManagedPolicyArns: Optional[Resolvable[List[ResolvableStr]]] = None
    Path: Optional[ResolvableStr] = None
    PermissionsBoundary: Optional[ResolvableStr] = None
    Policies: Optional[Resolvable[List[Resolvable[Policy]]]] = None
    UserName: Optional[ResolvableStr] = None


class IAMUser(Resource):
    TYPE_VALUE: ClassVar = "AWS::IAM::User"
    Type: str = TYPE_VALUE
    Properties: Optional[Resolvable[IAMUserProperties]]

    def has_hardcoded_credentials(self) -> bool:
        if self.Properties:
            login_profile = self.Properties.LoginProfile
            if login_profile and login_profile.get("Password"):
                if login_profile["Password"] != Parameter.NO_ECHO_NO_DEFAULT:
                    return True

        return super().has_hardcoded_credentials()
