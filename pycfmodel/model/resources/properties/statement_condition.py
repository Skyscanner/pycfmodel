import binascii
import logging
from base64 import b64decode
from typing import Any, Callable, Dict, Optional, Tuple, Union
from unicodedata import normalize

from pydantic import root_validator, validator

from pycfmodel.model.base import CustomModel, FunctionDict
from pycfmodel.model.types import (
    ResolvableArnOrList,
    ResolvableBool,
    ResolvableBoolOrList,
    ResolvableBytesOrList,
    ResolvableDatetimeOrList,
    ResolvableIntOrList,
    ResolvableIPOrList,
    ResolvableStrOrList,
)
from pycfmodel.utils import convert_to_list, is_resolvable_dict, not_ip, regex_from_cf_string

logger = logging.getLogger(__name__)


class StatementConditionBuildEvaluatorError(Exception):
    pass


def build_evaluator(function: str, arg_a: Any, arg_b: Any) -> Callable:
    if is_resolvable_dict(arg_b) or isinstance(arg_b, FunctionDict):
        raise StatementConditionBuildEvaluatorError

    if function == "Bool":
        return lambda kwargs: kwargs[arg_a] is arg_b

    elif function == "IpAddress":
        if not_ip(arg_b):
            return lambda _: False
        return lambda kwargs: kwargs[arg_a].subnet_of(arg_b)
    elif function == "NotIpAddress":
        if not_ip(arg_b):
            return lambda _: False
        return lambda kwargs: not kwargs[arg_a].subnet_of(arg_b)

    elif function == "Null":
        return lambda kwargs: (kwargs.get(arg_a) is not None) is arg_b

    elif function in ("StringEquals", "ArnEquals", "BinaryEquals", "NumericEquals", "DateEquals"):
        return lambda kwargs: kwargs[arg_a] == arg_b
    elif function in ("StringNotEquals", "ArnNotEquals", "NumericNotEquals", "DateNotEquals"):
        return lambda kwargs: kwargs[arg_a] != arg_b

    elif function in ("NumericLessThan", "DateLessThan"):
        return lambda kwargs: kwargs[arg_a] < arg_b
    elif function in ("NumericLessThanEquals", "DateLessThanEquals"):
        return lambda kwargs: kwargs[arg_a] <= arg_b
    elif function in ("NumericGreaterThan", "DateGreaterThan"):
        return lambda kwargs: kwargs[arg_a] > arg_b
    elif function in ("NumericGreaterThanEquals", "DateGreaterThanEquals"):
        return lambda kwargs: kwargs[arg_a] >= arg_b

    elif function == "StringEqualsIgnoreCase":
        arg_b = normalize("NFKD", arg_b.casefold())
        return lambda kwargs: normalize("NFKD", kwargs[arg_a].casefold()) == arg_b
    elif function == "StringNotEqualsIgnoreCase":
        arg_b = normalize("NFKD", arg_b.casefold())
        return lambda kwargs: normalize("NFKD", kwargs[arg_a].casefold()) != arg_b
    elif function in ("StringLike", "ArnLike"):
        arg_b = regex_from_cf_string(arg_b)
        return lambda kwargs: bool(arg_b.match(kwargs[arg_a]))
    elif function in ("StringNotLike", "ArnNotLike"):
        arg_b = regex_from_cf_string(arg_b)
        return lambda kwargs: not bool(arg_b.match(kwargs[arg_a]))
    else:
        logger.error(f"{function} is not supported.")
        raise NotImplementedError


def build_root_evaluator(function: str, arguments: Union[Dict, Tuple]) -> Callable:
    if isinstance(arguments, dict):
        arguments = arguments.items()
    elif isinstance(arguments, tuple):
        arguments = [arguments]

    if function.endswith("IfExists"):
        new_function = function.replace("IfExists", "")
    elif function.startswith("ForAllValues"):
        new_function = function.replace("ForAllValues", "")
    elif function.startswith("ForAnyValue"):
        new_function = function.replace("ForAnyValue", "")
    else:
        new_function = function

    group_of_nodes = []
    for arg_a, arg_b in arguments:
        if function.endswith("IfExists"):
            node = build_root_evaluator(new_function, (arg_a, arg_b))
            group_of_nodes.append(lambda kwargs: node(kwargs) if kwargs.get(arg_a) is not None else True)
        elif function.startswith("ForAllValues"):
            nodes = [build_root_evaluator(new_function, (arg_a, item)) for item in convert_to_list(arg_b)]
            all_nodes = lambda kwargs: any(node(kwargs) for node in nodes)  # noqa: E731
            group_of_nodes.append(
                lambda kwargs: all(all_nodes({**kwargs, arg_a: item}) for item in convert_to_list(kwargs[arg_a]))
            )
        elif function.startswith("ForAnyValue") or isinstance(arg_b, list):
            nodes = [build_root_evaluator(new_function, (arg_a, item)) for item in convert_to_list(arg_b)]
            all_nodes = lambda kwargs: any(node(kwargs) for node in nodes)  # noqa: E731
            group_of_nodes.append(
                lambda kwargs: any(all_nodes({**kwargs, arg_a: item}) for item in convert_to_list(kwargs[arg_a]))
            )
        else:
            group_of_nodes.append(build_evaluator(new_function, arg_a, arg_b))

    return lambda kwargs: all(group(kwargs) for group in group_of_nodes)


class StatementCondition(CustomModel):
    """
    Contains the condition to be matched to apply the statement that belongs to.

    | Type                       | Operators                 | ...IfExists | ForAllValues... | ForAnyValue... |
    | -------------------------- | ------------------------- | ----------- | --------------- | -------------- |
    | String                     | StringEquals              | Yes         | Yes             | Yes            |
    | String                     | StringNotEquals           | Yes         | Yes             | Yes            |
    | String                     | StringEqualsIgnoreCase    | Yes         | Yes             | Yes            |
    | String                     | StringNotEqualsIgnoreCase | Yes         | Yes             | Yes            |
    | String                     | StringLike                | Yes         | Yes             | Yes            |
    | String                     | StringNotLike             | Yes         | Yes             | Yes            |
    | Numeric                    | NumericEquals             | Yes         | Yes             | Yes            |
    | Numeric                    | NumericNotEquals          | Yes         | Yes             | Yes            |
    | Numeric                    | NumericLessThan           | Yes         | Yes             | Yes            |
    | Numeric                    | NumericLessThanEquals     | Yes         | Yes             | Yes            |
    | Numeric                    | NumericGreaterThan        | Yes         | Yes             | Yes            |
    | Numeric                    | NumericGreaterThanEquals  | Yes         | Yes             | Yes            |
    | Date and time              | DateEquals                | Yes         | Yes             | Yes            |
    | Date and time              | DateNotEquals             | Yes         | Yes             | Yes            |
    | Date and time              | DateLessThan              | Yes         | Yes             | Yes            |
    | Date and time              | DateLessThanEquals        | Yes         | Yes             | Yes            |
    | Date and time              | DateGreaterThan           | Yes         | Yes             | Yes            |
    | Date and time              | DateGreaterThanEquals     | Yes         | Yes             | Yes            |
    | Boolean                    | Bool                      | Yes         | Yes             | Yes            |
    | Binary                     | BinaryEquals              | Yes         | Yes             | Yes            |
    | IP address                 | IpAddress                 | Yes         | Yes             | Yes            |
    | IP address                 | NotIpAddress              | Yes         | Yes             | Yes            |
    | Amazon Resource Name (ARN) | ArnEquals                 | Yes         | Yes             | Yes            |
    | Amazon Resource Name (ARN) | ArnLike                   | Yes         | Yes             | Yes            |
    | Amazon Resource Name (ARN) | ArnNotEquals              | Yes         | Yes             | Yes            |
    | Amazon Resource Name (ARN) | ArnNotLike                | Yes         | Yes             | Yes            |
    | Existence                  | Null                      | No          | Yes             | Yes            |

    Table based on [AWS Docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html)

    For conditions such as `StringEquals` with multiple values for one key, we evaluate them using the logical `OR`,
    similar to if the condition key was `ForAnyValue:StringEquals`. This follows the
    [documentation from AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_multi-value-conditions.html).
    """

    ArnEquals: Optional[Dict[str, ResolvableArnOrList]]
    ArnLike: Optional[Dict[str, ResolvableArnOrList]]
    ArnNotEquals: Optional[Dict[str, ResolvableArnOrList]]
    ArnNotLike: Optional[Dict[str, ResolvableArnOrList]]
    ArnEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ArnLikeIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ArnNotEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ArnNotLikeIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnEquals: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnLike: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnNotEquals: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnNotLike: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnLikeIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnNotEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAllValuesArnNotLikeIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnEquals: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnLike: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnNotEquals: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnNotLike: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnLikeIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnNotEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]]
    ForAnyValueArnNotLikeIfExists: Optional[Dict[str, ResolvableArnOrList]]

    Bool: Optional[Dict[str, ResolvableBoolOrList]]
    BoolIfExists: Optional[Dict[str, ResolvableBoolOrList]]
    ForAllValuesBool: Optional[Dict[str, ResolvableBoolOrList]]
    ForAllValuesBoolIfExists: Optional[Dict[str, ResolvableBoolOrList]]
    ForAnyValueBool: Optional[Dict[str, ResolvableBoolOrList]]
    ForAnyValueBoolIfExists: Optional[Dict[str, ResolvableBoolOrList]]

    BinaryEquals: Optional[Dict[str, ResolvableBytesOrList]]
    BinaryEqualsIfExists: Optional[Dict[str, ResolvableBytesOrList]]
    ForAllValuesBinaryEquals: Optional[Dict[str, ResolvableBytesOrList]]
    ForAllValuesBinaryEqualsIfExists: Optional[Dict[str, ResolvableBytesOrList]]
    ForAnyValueBinaryEquals: Optional[Dict[str, ResolvableBytesOrList]]
    ForAnyValueBinaryEqualsIfExists: Optional[Dict[str, ResolvableBytesOrList]]

    DateEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateNotEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateLessThan: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateLessThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateGreaterThan: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateGreaterThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateNotEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateLessThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateLessThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateGreaterThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    DateGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateNotEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateLessThan: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateLessThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateGreaterThan: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateGreaterThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateNotEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateLessThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateLessThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateGreaterThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAllValuesDateGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateNotEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateLessThan: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateLessThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateGreaterThan: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateGreaterThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateNotEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateLessThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateLessThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateGreaterThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]
    ForAnyValueDateGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]]

    IpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    NotIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    IpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    NotIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAllValuesIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAllValuesNotIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAnyValueIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAnyValueNotIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAllValuesIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAllValuesNotIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAnyValueIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]
    ForAnyValueNotIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]]

    Null: Optional[Dict[str, ResolvableBool]]
    ForAllValuesNull: Optional[Dict[str, ResolvableBool]]
    ForAnyValueNull: Optional[Dict[str, ResolvableBool]]

    NumericEquals: Optional[Dict[str, ResolvableIntOrList]]
    NumericNotEquals: Optional[Dict[str, ResolvableIntOrList]]
    NumericLessThan: Optional[Dict[str, ResolvableIntOrList]]
    NumericLessThanEquals: Optional[Dict[str, ResolvableIntOrList]]
    NumericGreaterThan: Optional[Dict[str, ResolvableIntOrList]]
    NumericGreaterThanEquals: Optional[Dict[str, ResolvableIntOrList]]
    NumericEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    NumericNotEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    NumericLessThanIfExists: Optional[Dict[str, ResolvableIntOrList]]
    NumericLessThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    NumericGreaterThanIfExists: Optional[Dict[str, ResolvableIntOrList]]
    NumericGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericNotEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericLessThan: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericLessThanEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericGreaterThan: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericGreaterThanEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericNotEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericLessThanIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericLessThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericGreaterThanIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAllValuesNumericGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericNotEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericLessThan: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericLessThanEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericGreaterThan: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericGreaterThanEquals: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericNotEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericLessThanIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericLessThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericGreaterThanIfExists: Optional[Dict[str, ResolvableIntOrList]]
    ForAnyValueNumericGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]]

    StringEquals: Optional[Dict[str, ResolvableStrOrList]]
    StringNotEquals: Optional[Dict[str, ResolvableStrOrList]]
    StringEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]]
    StringNotEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]]
    StringLike: Optional[Dict[str, ResolvableStrOrList]]
    StringNotLike: Optional[Dict[str, ResolvableStrOrList]]
    StringEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]]
    StringNotEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]]
    StringEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]]
    StringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]]
    StringLikeIfExists: Optional[Dict[str, ResolvableStrOrList]]
    StringNotLikeIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringEquals: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringNotEquals: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringNotEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringLike: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringNotLike: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringNotEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringLikeIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAllValuesStringNotLikeIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringEquals: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringNotEquals: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringNotEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringLike: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringNotLike: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringNotEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringLikeIfExists: Optional[Dict[str, ResolvableStrOrList]]
    ForAnyValueStringNotLikeIfExists: Optional[Dict[str, ResolvableStrOrList]]

    _eval: Optional[Callable] = None

    @root_validator(pre=True)
    def remove_colon(cls, values):
        return {key.replace(":", ""): value for key, value in values.items()}

    @validator(
        "BinaryEquals",
        "BinaryEqualsIfExists",
        "ForAllValuesBinaryEquals",
        "ForAllValuesBinaryEqualsIfExists",
        "ForAnyValueBinaryEquals",
        "ForAnyValueBinaryEqualsIfExists",
        each_item=True,
        pre=True,
    )
    def validate_binary(cls, value: Any) -> bytearray:
        try:
            value = b64decode(value)
        except binascii.Error:
            raise ValueError("Binary value not valid")
        return value

    def eval(self, values):
        if self._eval is None:
            self._eval = self.build_eval(self.dict())
        return self._eval(values)

    @classmethod
    def build_eval(cls, values: Dict) -> Dict:
        conditions_lambdas = [
            build_root_evaluator(function=key, arguments=value) for key, value in values.items() if value is not None
        ]
        return lambda kwargs: all(condition(kwargs) for condition in conditions_lambdas)

    def __call__(self, kwargs) -> Optional[bool]:
        try:
            return self.eval(kwargs)
        except Exception:
            logger.exception("Error raised while evaluating condition")
            return None

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.dict(exclude_unset={"eval"}) == other.dict(exclude_unset={"eval"})
        else:
            return self.dict() == other
