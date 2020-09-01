from typing import List, Optional, Pattern, Union

from pydantic import Extra

from pycfmodel.action_expander import _expand_action
from pycfmodel.cloudformation_actions import CLOUDFORMATION_ACTIONS
from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.resources.properties.statement import Statement
from pycfmodel.model.types import Resolvable, ResolvableDate


class PolicyDocument(Property):
    """
    Contains information about an attached policy.

    Properties:

    - Statement: A [statement][pycfmodel.model.resources.properties.statement.Statement] object.
    - Version
    """

    class Config(Property.Config):
        extra = Extra.allow

    Statement: Resolvable[Union[Statement, List[Resolvable[Statement]]]]
    Version: Optional[ResolvableDate] = None

    def _statement_as_list(self) -> List[Statement]:
        if isinstance(self.Statement, Statement):
            return [self.Statement]
        return self.Statement

    def statements_with(self, pattern: Pattern) -> List[Statement]:
        """
        Finds all statements which have at least one resource with the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of [statements][pycfmodel.model.resources.properties.statement.Statement].
        """
        return [statement for statement in self._statement_as_list() if statement.resources_with(pattern)]

    def allowed_actions_with(self, pattern: Pattern) -> List[Statement]:
        """
        Finds all statements which have at least one action with the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of [statements][pycfmodel.model.resources.properties.statement.Statement].
        """
        return [
            statement
            for statement in self._statement_as_list()
            if statement.actions_with(pattern) and statement.Effect == "Allow"
        ]

    def allowed_principals_with(self, pattern: Pattern) -> List[str]:
        """
        Finds all allowed principals which match the pattern.

        Arguments:
            pattern: Pattern to match.

        Returns:
            List of principals.
        """
        principals = set()
        for statement in self._statement_as_list():
            if statement.Effect == "Allow":
                principals.update(statement.principals_with(pattern))
        return list(principals)

    def non_whitelisted_allowed_principals(self, whitelist: List[str]) -> List[str]:
        """
        Find non whitelisted allowed principals.

        Arguments:
            whitelist: List of whitelisted principals.

        Returns:
            List of principals.
        """
        principals = set()
        for statement in self._statement_as_list():
            if statement.Effect == "Allow":
                principals.update(statement.non_whitelisted_principals(whitelist))
        return list(principals)

    def get_iam_actions(self, difference=False) -> List[str]:
        """
        Find all IAM Actions which are specified in statements.

        Arguments:
            difference: when True, the behaviour changes to find the difference between all IAM Actions and those specified in the statements of the policy. Default = False.

        Returns:
            List of matching actions.
        """
        actions = set()
        for statement in self._statement_as_list():
            for action in statement.get_action_list():
                if not isinstance(action, str):
                    continue

                for expanded_action in _expand_action(action):
                    if expanded_action.lower().startswith("iam:"):
                        actions.add(expanded_action)

        if difference:
            return sorted(
                set([action for action in CLOUDFORMATION_ACTIONS if action.lower().startswith("iam:")]).difference(
                    actions
                )
            )

        return sorted(actions)
