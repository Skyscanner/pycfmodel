from typing import List, Optional, Any, ClassVar

from pydantic import PositiveInt

from pycfmodel.model.base import CustomModel


class Parameter(CustomModel):
    """
    The class responsible for loading Jinja templates and rendering them.
    It defines some configuration options, implements the `render` method,
    and overrides the `update_env` method of the [`BaseRenderer` class][mkdocstrings.handlers.BaseRenderer].
    """

    NO_ECHO_NO_DEFAULT: ClassVar[str] = "NO_ECHO_NO_DEFAULT"
    NO_ECHO_WITH_DEFAULT: ClassVar[str] = "NO_ECHO_WITH_DEFAULT"
    NO_ECHO_WITH_VALUE: ClassVar[str] = "NO_ECHO_WITH_VALUE"
    AllowedPattern: Optional[str] = None
    AllowedValues: Optional[List] = None
    ConstraintDescription: Optional[str] = None
    Default: Optional[Any] = None
    Description: Optional[str] = None
    MaxLength: Optional[PositiveInt] = None
    MaxValue: Optional[PositiveInt] = None
    MinLength: Optional[int] = None
    MinValue: Optional[int] = None
    NoEcho: Optional[bool] = None
    Type: str

    def get_ref_value(self, provided_value=None) -> Optional[str]:
        """


        Arguments:
            provided_value: An XML node, used like the root of an XML tree.

        Returns:
            The same node, recursively modified by side-effect. You can skip re-assigning the return value.
        """
        value = provided_value if provided_value is not None else self.Default
        if self.NoEcho:
            if provided_value is not None:
                return self.NO_ECHO_WITH_VALUE
            elif self.Default:
                return self.NO_ECHO_WITH_DEFAULT
            else:
                return self.NO_ECHO_NO_DEFAULT

        elif self.Type in ["List<Number>", "CommaDelimitedList"]:
            return value.split(",")

        return value if value is None else str(value)
