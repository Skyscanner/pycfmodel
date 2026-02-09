import logging
from typing import Any, Callable, Dict, Optional, Tuple, Union
from unicodedata import normalize

from pydantic import model_validator

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

    ArnEquals: Optional[Dict[str, ResolvableArnOrList]] = None
    ArnLike: Optional[Dict[str, ResolvableArnOrList]] = None
    ArnNotEquals: Optional[Dict[str, ResolvableArnOrList]] = None
    ArnNotLike: Optional[Dict[str, ResolvableArnOrList]] = None
    ArnEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ArnLikeIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ArnNotEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ArnNotLikeIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnEquals: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnLike: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnNotEquals: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnNotLike: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnLikeIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnNotEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAllValuesArnNotLikeIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnEquals: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnLike: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnNotEquals: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnNotLike: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnLikeIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnNotEqualsIfExists: Optional[Dict[str, ResolvableArnOrList]] = None
    ForAnyValueArnNotLikeIfExists: Optional[Dict[str, ResolvableArnOrList]] = None

    Bool: Optional[Dict[str, ResolvableBoolOrList]] = None
    BoolIfExists: Optional[Dict[str, ResolvableBoolOrList]] = None
    ForAllValuesBool: Optional[Dict[str, ResolvableBoolOrList]] = None
    ForAllValuesBoolIfExists: Optional[Dict[str, ResolvableBoolOrList]] = None
    ForAnyValueBool: Optional[Dict[str, ResolvableBoolOrList]] = None
    ForAnyValueBoolIfExists: Optional[Dict[str, ResolvableBoolOrList]] = None

    BinaryEquals: Optional[Dict[str, ResolvableBytesOrList]] = None
    BinaryEqualsIfExists: Optional[Dict[str, ResolvableBytesOrList]] = None
    ForAllValuesBinaryEquals: Optional[Dict[str, ResolvableBytesOrList]] = None
    ForAllValuesBinaryEqualsIfExists: Optional[Dict[str, ResolvableBytesOrList]] = None
    ForAnyValueBinaryEquals: Optional[Dict[str, ResolvableBytesOrList]] = None
    ForAnyValueBinaryEqualsIfExists: Optional[Dict[str, ResolvableBytesOrList]] = None

    DateEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateNotEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateLessThan: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateLessThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateGreaterThan: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateGreaterThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateNotEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateLessThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateLessThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateGreaterThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    DateGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateNotEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateLessThan: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateLessThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateGreaterThan: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateGreaterThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateNotEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateLessThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateLessThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateGreaterThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAllValuesDateGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateNotEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateLessThan: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateLessThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateGreaterThan: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateGreaterThanEquals: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateNotEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateLessThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateLessThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateGreaterThanIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None
    ForAnyValueDateGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableDatetimeOrList]] = None

    IpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    NotIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    IpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    NotIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAllValuesIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAllValuesNotIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAnyValueIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAnyValueNotIpAddress: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAllValuesIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAllValuesNotIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAnyValueIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None
    ForAnyValueNotIpAddressIfExists: Optional[Dict[str, Union[ResolvableIPOrList, ResolvableStrOrList]]] = None

    Null: Optional[Dict[str, ResolvableBool]] = None
    ForAllValuesNull: Optional[Dict[str, ResolvableBool]] = None
    ForAnyValueNull: Optional[Dict[str, ResolvableBool]] = None

    NumericEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericNotEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericLessThan: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericLessThanEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericGreaterThan: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericGreaterThanEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericNotEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericLessThanIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericLessThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericGreaterThanIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    NumericGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericNotEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericLessThan: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericLessThanEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericGreaterThan: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericGreaterThanEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericNotEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericLessThanIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericLessThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericGreaterThanIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAllValuesNumericGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericNotEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericLessThan: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericLessThanEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericGreaterThan: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericGreaterThanEquals: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericNotEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericLessThanIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericLessThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericGreaterThanIfExists: Optional[Dict[str, ResolvableIntOrList]] = None
    ForAnyValueNumericGreaterThanEqualsIfExists: Optional[Dict[str, ResolvableIntOrList]] = None

    StringEquals: Optional[Dict[str, ResolvableStrOrList]] = None
    StringNotEquals: Optional[Dict[str, ResolvableStrOrList]] = None
    StringEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]] = None
    StringNotEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]] = None
    StringLike: Optional[Dict[str, ResolvableStrOrList]] = None
    StringNotLike: Optional[Dict[str, ResolvableStrOrList]] = None
    StringEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    StringNotEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    StringEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    StringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    StringLikeIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    StringNotLikeIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringEquals: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringNotEquals: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringNotEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringLike: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringNotLike: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringNotEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringLikeIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAllValuesStringNotLikeIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringEquals: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringNotEquals: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringNotEqualsIgnoreCase: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringLike: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringNotLike: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringNotEqualsIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringLikeIfExists: Optional[Dict[str, ResolvableStrOrList]] = None
    ForAnyValueStringNotLikeIfExists: Optional[Dict[str, ResolvableStrOrList]] = None

    _eval: Optional[Callable] = None

    @model_validator(mode="before")
    @classmethod
    def remove_colon(cls, values):
        if isinstance(values, dict):
            return {key.replace(":", ""): value for key, value in values.items()}
        return values

    def eval(self, values):
        if self._eval is None:
            self._eval = self.build_eval(self.model_dump())
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
            return self.model_dump(exclude={"eval"}) == other.model_dump(exclude={"eval"})
        else:
            return self.model_dump() == other
