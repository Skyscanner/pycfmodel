from typing import List, Optional, Any, ClassVar

from pydantic import PositiveInt

from pycfmodel.model.base import CustomModel


class Parameter(CustomModel):
    """
    CloudFormation Parameter object representation
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
        Calculates the parameter value to be used in the template.

        - If `NoEcho` property is set, it uses a constant value.
        - If it is a list of numbers or a comma delimited list, returns the string version of each element in a list.
        - Returns None if `provided_value` and `Default` are `None`.

        Arguments:
            provided_value: Value injected in the template

        Returns:
            The computed value.
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
