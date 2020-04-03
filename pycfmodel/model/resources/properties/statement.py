import logging

from typing import List, Pattern, Optional, Union, Dict

from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.types import ResolvableStr, ResolvableStrOrList
from pycfmodel.utils import is_resolvable_dict

logger = logging.getLogger(__file__)

PrincipalTypes = Union[ResolvableStr, List[ResolvableStr], Dict[str, Union[ResolvableStr, List[ResolvableStr]]]]


class Statement(Property):
    """
    Contains information about an attached policy.

    Properties:

    - Sid: Optional identifier.
    - Effect: Whether the statement results in an allow or an explicit deny.
    - Principal: Specify the IAM user, federated user, IAM role, AWS account, AWS service, or other principal that is allowed to access a resource.
    - NotPrincipal: Specify the IAM user, federated user, IAM role, AWS account, AWS service, or other principal that is not allowed or denied access to a resource.
    - Action: Specific action or actions that will be allowed or denied.
    - NotAction: Explicitly matches everything except the specified action or list of actions.
    - Resource: Specifies the object or objects that the statement covers.
    - NotResource: Specifies the object or objects that the statement does not cover.

    More info at [AWS Docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)
    """

    Sid: Optional[ResolvableStr] = None
    Effect: Optional[ResolvableStr] = None
    Principal: Optional[PrincipalTypes] = None
    NotPrincipal: Optional[PrincipalTypes] = None
    Action: Optional[ResolvableStrOrList] = None
    NotAction: Optional[ResolvableStrOrList] = None
    Resource: Optional[ResolvableStrOrList] = None
    NotResource: Optional[ResolvableStrOrList] = None

    def get_action_list(self) -> List[ResolvableStr]:
        """
        Gets all actions specified in `Action` and `NotAction`.

        Returns:
            List of actions.
        """
        action_list = []
        for actions in [self.Action, self.NotAction]:
            if isinstance(actions, List):
                action_list.extend(actions)
            elif isinstance(actions, (str, dict)):
                action_list.append(actions)
        return action_list

    def get_resource_list(self) -> List[ResolvableStr]:
        """
        Gets all resources specified in `Resource` and `NotResource`.

        Returns:
            List of resources.
        """
        resource_list = []
        for resources in [self.Resource, self.NotResource]:
            if isinstance(resources, List):
                resource_list.extend(resources)
            elif isinstance(resources, (str, dict)):
                resource_list.append(resources)
        return resource_list

    def get_principal_list(self) -> List[ResolvableStr]:
        """
        Gets all actions specified in `Principal` and `NotPrincipal`.

        Returns:
            List of principals.
        """
        principal_list = []
        for principals in [self.Principal, self.NotPrincipal]:
            if isinstance(principals, list):
                principal_list.extend(principals)
            elif isinstance(principals, str):
                principal_list.append(principals)
            elif is_resolvable_dict(principals):
                principal_list.append(principals)
            elif isinstance(principals, dict):
                for value in principals.values():
                    if isinstance(value, (str, Dict)):
                        principal_list.append(value)
                    elif isinstance(value, List):
                        principal_list.extend(value)
            elif principals is not None:
                raise ValueError(f"Not supported type: {type(principals)}")
        return principal_list

    def actions_with(self, pattern: Pattern) -> List[str]:
        """
        Finds all actions which match the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of actions.
        """
        return [action for action in self.get_action_list() if isinstance(action, str) and pattern.match(action)]

    def principals_with(self, pattern: Pattern) -> List[str]:
        """
        Finds all principals which match the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of principals.
        """
        return [
            principal
            for principal in self.get_principal_list()
            if isinstance(principal, str) and pattern.match(principal)
        ]

    def resources_with(self, pattern: Pattern) -> List[str]:
        """
        Finds all resources which match the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of resources.
        """
        return [
            resource for resource in self.get_resource_list() if isinstance(resource, str) and pattern.match(resource)
        ]

    def non_whitelisted_principals(self, whitelist: List[str]) -> List[str]:
        """
        Find non whitelisted principals.

        Arguments:
            whitelist: List of whitelisted principals.

        Returns:
            List of principals.
        """
        return [
            principal
            for principal in self.get_principal_list()
            if isinstance(principal, str) and principal not in whitelist
        ]
