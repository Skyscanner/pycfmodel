import binascii
import logging
import re
from base64 import b64decode
from typing import Any, Callable, Dict, Optional, Tuple, Union
from unicodedata import normalize

from pydantic import BaseModel, root_validator, validator

from pycfmodel.model.base import FunctionDict
from pycfmodel.model.types import ARNOrList, BytesOrList, DatetimeOrList, IntOrList, IPOrList, StrOrList
from pycfmodel.utils import is_resolvable_dict

logger = logging.getLogger()


class StatementConditionBuildEvaluatorError(Exception):
    pass


def build_evaluator(function: str, arg_a: Any, arg_b: Any) -> Callable:
    if is_resolvable_dict(arg_b) or isinstance(arg_b, FunctionDict):
        raise StatementConditionBuildEvaluatorError

    if function == "Bool":
        return lambda kwargs: kwargs[arg_a] is arg_b

    elif function == "IpAddress":
        return lambda kwargs: kwargs[arg_a] in arg_b or kwargs[arg_a] == arg_b
    elif function == "NotIpAddress":
        return lambda kwargs: kwargs[arg_a] not in arg_b and kwargs[arg_a] != arg_b

    elif function == "Null":
        return lambda kwargs: (kwargs.get(arg_a) is None) is arg_b

    elif function in ("NumericEquals", "DateEquals"):
        return lambda kwargs: kwargs[arg_a] == arg_b
    elif function in ("NumericNotEquals", "DateNotEquals"):
        return lambda kwargs: kwargs[arg_a] != arg_b
    elif function in ("NumericLessThan", "DateLessThan"):
        return lambda kwargs: kwargs[arg_a] < arg_b
    elif function in ("NumericLessThanEquals", "DateLessThanEquals"):
        return lambda kwargs: kwargs[arg_a] <= arg_b
    elif function in ("NumericGreaterThan", "DateGreaterThan"):
        return lambda kwargs: kwargs[arg_a] > arg_b
    elif function in ("NumericGreaterThanEquals", "DateGreaterThanEquals"):
        return lambda kwargs: kwargs[arg_a] >= arg_b

    elif function in ("StringEquals", "ArnEquals", "BinaryEquals"):
        return lambda kwargs: kwargs[arg_a] == arg_b
    elif function in ("StringNotEquals", "ArnNotEquals"):
        return lambda kwargs: kwargs[arg_a] != arg_b
    elif function == "StringEqualsIgnoreCase":
        arg_b = normalize("NFKD", arg_b.casefold())
        return lambda kwargs: normalize("NFKD", kwargs[arg_a]) == arg_b
    elif function == "StringNotEqualsIgnoreCase":
        arg_b = normalize("NFKD", arg_b.casefold())
        return lambda kwargs: normalize("NFKD", kwargs[arg_a]) != arg_b
    elif function in ("StringLike", "ArnLike"):
        arg_b = re.compile(arg_b.replace("*", ".*"))
        return lambda kwargs: bool(arg_b.match(kwargs[arg_a]))
    elif function in ("StringNotLike", "ArnNotLike"):
        arg_b = re.compile(arg_b.replace("*", ".*"))
        return lambda kwargs: not bool(arg_b.match(kwargs[arg_a]))


def build_root_evaluator(function: str, arguments: Union[Dict, Tuple]) -> Callable:
    if isinstance(arguments, dict):
        arguments = arguments.items()
    elif isinstance(arguments, tuple):
        arguments = [arguments]

    if function.startswith("ForAllValues:"):
        new_function = function.replace("ForAllValues:", "")
    elif function.endswith("ForAnyValue:"):
        new_function = function.replace("ForAnyValue:", "")
    elif function.endswith("IfExists"):
        new_function = function.replace("IfExists", "")
    else:
        new_function = function

    group_of_nodes = []
    for arg_a, arg_b in arguments:
        if function.startswith("ForAllValues:"):
            nodes = [build_root_evaluator(new_function, (item, arg_b)) for item in arg_a]
            group_of_nodes.append(lambda kwargs: all(node(kwargs) for node in nodes))
        elif function.endswith("ForAnyValue:"):
            nodes = [build_root_evaluator(new_function, (item, arg_b)) for item in arg_a]
            group_of_nodes.append(lambda kwargs: any(node(kwargs) for node in nodes))
        elif function.endswith("IfExists"):
            node = build_root_evaluator(new_function, (arg_a, arg_b))
            group_of_nodes.append(lambda kwargs: kwargs.get(arg_a) is not None and node(kwargs))
        else:
            if isinstance(arg_b, list):
                nodes = [build_evaluator(new_function, arg_a, item) for item in arg_b]
                group_of_nodes.append(lambda kwargs: any(node(kwargs) for node in nodes))
            else:
                group_of_nodes.append(build_evaluator(new_function, arg_a, arg_b))

    return lambda kwargs: all(group(kwargs) for group in group_of_nodes)


class StatementCondition(BaseModel):
    ArnEquals: Optional[Dict[str, ARNOrList]]
    ArnLike: Optional[Dict[str, ARNOrList]]
    ArnNotEquals: Optional[Dict[str, ARNOrList]]
    ArnNotLike: Optional[Dict[str, ARNOrList]]
    ArnEqualsIfExists: Optional[Dict[str, ARNOrList]]
    ArnLikeIfExists: Optional[Dict[str, ARNOrList]]
    ArnNotEqualsIfExists: Optional[Dict[str, ARNOrList]]
    ArnNotLikeIfExists: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnEquals: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnLike: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnNotEquals: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnNotLike: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnEqualsIfExists: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnLikeIfExists: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnNotEqualsIfExists: Optional[Dict[str, ARNOrList]]
    ForAllValuesArnNotLikeIfExists: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnEquals: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnLike: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnNotEquals: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnNotLike: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnEqualsIfExists: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnLikeIfExists: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnNotEqualsIfExists: Optional[Dict[str, ARNOrList]]
    ForAnyValueArnNotLikeIfExists: Optional[Dict[str, ARNOrList]]

    Bool: Optional[Dict[str, bool]]
    BoolIfExists: Optional[Dict[str, bool]]
    ForAllValuesBool: Optional[Dict[str, bool]]
    ForAllValuesBoolIfExists: Optional[Dict[str, bool]]
    ForAnyValueBool: Optional[Dict[str, bool]]
    ForAnyValueBoolIfExists: Optional[Dict[str, bool]]

    BinaryEquals: Optional[Dict[str, BytesOrList]]
    BinaryEqualsIfExists: Optional[Dict[str, BytesOrList]]
    ForAllValuesBinaryEquals: Optional[Dict[str, BytesOrList]]
    ForAllValuesBinaryEqualsIfExists: Optional[Dict[str, BytesOrList]]
    ForAnyValueBinaryEquals: Optional[Dict[str, BytesOrList]]
    ForAnyValueBinaryEqualsIfExists: Optional[Dict[str, BytesOrList]]

    DateEquals: Optional[Dict[str, DatetimeOrList]]
    DateNotEquals: Optional[Dict[str, DatetimeOrList]]
    DateLessThan: Optional[Dict[str, DatetimeOrList]]
    DateLessThanEquals: Optional[Dict[str, DatetimeOrList]]
    DateGreaterThan: Optional[Dict[str, DatetimeOrList]]
    DateGreaterThanEquals: Optional[Dict[str, DatetimeOrList]]
    DateEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    DateNotEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    DateLessThanIfExists: Optional[Dict[str, DatetimeOrList]]
    DateLessThanEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    DateGreaterThanIfExists: Optional[Dict[str, DatetimeOrList]]
    DateGreaterThanEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateEquals: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateNotEquals: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateLessThan: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateLessThanEquals: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateGreaterThan: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateGreaterThanEquals: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateNotEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateLessThanIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateLessThanEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateGreaterThanIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAllValuesDateGreaterThanEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateEquals: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateNotEquals: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateLessThan: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateLessThanEquals: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateGreaterThan: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateGreaterThanEquals: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateNotEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateLessThanIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateLessThanEqualsIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateGreaterThanIfExists: Optional[Dict[str, DatetimeOrList]]
    ForAnyValueDateGreaterThanEqualsIfExists: Optional[Dict[str, DatetimeOrList]]

    IpAddress: Optional[Dict[str, IPOrList]]
    NotIpAddress: Optional[Dict[str, IPOrList]]
    ForAllValuesIpAddressIfExists: Optional[Dict[str, IPOrList]]
    ForAllValuesNotIpAddressIfExists: Optional[Dict[str, IPOrList]]
    ForAnyValueIpAddressIfExists: Optional[Dict[str, IPOrList]]
    ForAnyValueNotIpAddressIfExists: Optional[Dict[str, IPOrList]]

    Null: Optional[Dict[str, bool]]
    ForAllValuesNull: Optional[Dict[str, bool]]
    ForAnyValueNull: Optional[Dict[str, bool]]

    NumericEquals: Optional[Dict[str, IntOrList]]
    NumericNotEquals: Optional[Dict[str, IntOrList]]
    NumericLessThan: Optional[Dict[str, IntOrList]]
    NumericLessThanEquals: Optional[Dict[str, IntOrList]]
    NumericGreaterThan: Optional[Dict[str, IntOrList]]
    NumericGreaterThanEquals: Optional[Dict[str, IntOrList]]
    NumericEqualsIfExists: Optional[Dict[str, IntOrList]]
    NumericNotEqualsIfExists: Optional[Dict[str, IntOrList]]
    NumericLessThanIfExists: Optional[Dict[str, IntOrList]]
    NumericLessThanEqualsIfExists: Optional[Dict[str, IntOrList]]
    NumericGreaterThanIfExists: Optional[Dict[str, IntOrList]]
    NumericGreaterThanEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericEquals: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericNotEquals: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericLessThan: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericLessThanEquals: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericGreaterThan: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericGreaterThanEquals: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericNotEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericLessThanIfExists: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericLessThanEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericGreaterThanIfExists: Optional[Dict[str, IntOrList]]
    ForAllValuesNumericGreaterThanEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericEquals: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericNotEquals: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericLessThan: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericLessThanEquals: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericGreaterThan: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericGreaterThanEquals: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericNotEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericLessThanIfExists: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericLessThanEqualsIfExists: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericGreaterThanIfExists: Optional[Dict[str, IntOrList]]
    ForAnyValueNumericGreaterThanEqualsIfExists: Optional[Dict[str, IntOrList]]

    StringEquals: Optional[Dict[str, StrOrList]]
    StringNotEquals: Optional[Dict[str, StrOrList]]
    StringEqualsIgnoreCase: Optional[Dict[str, StrOrList]]
    StringNotEqualsIgnoreCase: Optional[Dict[str, StrOrList]]
    StringLike: Optional[Dict[str, StrOrList]]
    StringNotLike: Optional[Dict[str, StrOrList]]
    StringEqualsIfExists: Optional[Dict[str, StrOrList]]
    StringNotEqualsIfExists: Optional[Dict[str, StrOrList]]
    StringEqualsIgnoreCaseIfExists: Optional[Dict[str, StrOrList]]
    StringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, StrOrList]]
    StringLikeIfExists: Optional[Dict[str, StrOrList]]
    StringNotLikeIfExists: Optional[Dict[str, StrOrList]]
    ForAllValuesStringEquals: Optional[Dict[str, StrOrList]]
    ForAllValuesStringNotEquals: Optional[Dict[str, StrOrList]]
    ForAllValuesStringEqualsIgnoreCase: Optional[Dict[str, StrOrList]]
    ForAllValuesStringNotEqualsIgnoreCase: Optional[Dict[str, StrOrList]]
    ForAllValuesStringLike: Optional[Dict[str, StrOrList]]
    ForAllValuesStringNotLike: Optional[Dict[str, StrOrList]]
    ForAllValuesStringEqualsIfExists: Optional[Dict[str, StrOrList]]
    ForAllValuesStringNotEqualsIfExists: Optional[Dict[str, StrOrList]]
    ForAllValuesStringEqualsIgnoreCaseIfExists: Optional[Dict[str, StrOrList]]
    ForAllValuesStringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, StrOrList]]
    ForAllValuesStringLikeIfExists: Optional[Dict[str, StrOrList]]
    ForAllValuesStringNotLikeIfExists: Optional[Dict[str, StrOrList]]
    ForAnyValueStringEquals: Optional[Dict[str, StrOrList]]
    ForAnyValueStringNotEquals: Optional[Dict[str, StrOrList]]
    ForAnyValueStringEqualsIgnoreCase: Optional[Dict[str, StrOrList]]
    ForAnyValueStringNotEqualsIgnoreCase: Optional[Dict[str, StrOrList]]
    ForAnyValueStringLike: Optional[Dict[str, StrOrList]]
    ForAnyValueStringNotLike: Optional[Dict[str, StrOrList]]
    ForAnyValueStringEqualsIfExists: Optional[Dict[str, StrOrList]]
    ForAnyValueStringNotEqualsIfExists: Optional[Dict[str, StrOrList]]
    ForAnyValueStringEqualsIgnoreCaseIfExists: Optional[Dict[str, StrOrList]]
    ForAnyValueStringNotEqualsIgnoreCaseIfExists: Optional[Dict[str, StrOrList]]
    ForAnyValueStringLikeIfExists: Optional[Dict[str, StrOrList]]
    ForAnyValueStringNotLikeIfExists: Optional[Dict[str, StrOrList]]

    eval: Optional[Callable]

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
    def validate_binary(cls, value):
        try:
            value = b64decode(value)
        except binascii.Error:
            raise ValueError(f"Binary value not valid")
        return value

    @root_validator()
    def build_eval(cls, values):
        try:
            conditions_lambdas = [
                build_root_evaluator(function=key, arguments=value)
                for key, value in values.items()
                if value is not None
            ]
            values["eval"] = lambda kwargs: all(condition(kwargs) for condition in conditions_lambdas)
        except StatementConditionBuildEvaluatorError:
            values["eval"] = lambda kwargs: (_ for _ in ()).throw(StatementConditionBuildEvaluatorError)
            logger.error("Resolvable function found. Try resolving the model...")
        return values

    def __call__(self, kwargs) -> Optional[bool]:
        try:
            return self.eval(kwargs)
        except Exception:
            logger.exception("Error raised while evaluating condition")
            return None
