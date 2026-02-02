"""
IAMInstanceProfile resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::IAM::InstanceProfile.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr


class IAMInstanceProfileProperties(CustomModel):
    """
    Properties for AWS::IAM::InstanceProfile.

    Properties:

    - InstanceProfileName: The name of the instance profile to create.
 This parameter allows (through its ...
    - Path: The path to the instance profile. For more information about paths, see [IAM Ide...
    - Roles: The name of the role to associate with the instance profile. Only one role can b...

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html)
    """

    Roles: Resolvable[List[ResolvableStr]]
    InstanceProfileName: Optional[ResolvableStr] = None
    Path: Optional[ResolvableStr] = None


class IAMInstanceProfile(Resource):
    """
    Creates a new instance profile. For information about instance profiles, see [Using instance profiles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html).
  For information about the number of instance profiles you can create, see [object quotas](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html) in the *User Guide*.

    Properties:

    - Properties: A [IAMInstanceProfileProperties][pycfmodel.model.resources.iam_instance_profile.IAMInstanceProfileProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html)
    """

    Type: Literal["AWS::IAM::InstanceProfile"]
    Properties: Resolvable[IAMInstanceProfileProperties]
