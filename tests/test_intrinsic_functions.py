"""Tests for CloudFormation intrinsic function validation."""

import pytest
from pydantic import ValidationError

from pycfmodel.model.base import FunctionDict
from pycfmodel.model.intrinsic_functions import (
    validate_condition,
    validate_fn_and,
    validate_fn_base64,
    validate_fn_equals,
    validate_fn_find_in_map,
    validate_fn_get_att,
    validate_fn_get_azs,
    validate_fn_if,
    validate_fn_import_value,
    validate_fn_join,
    validate_fn_not,
    validate_fn_or,
    validate_fn_select,
    validate_fn_split,
    validate_fn_sub,
    validate_intrinsic_function,
    validate_ref,
)


class TestRefValidation:
    def test_valid_ref(self):
        is_valid, error = validate_ref("MyResource")
        assert is_valid is True
        assert error is None

    def test_valid_ref_pseudo_parameter(self):
        is_valid, error = validate_ref("AWS::StackName")
        assert is_valid is True

    def test_invalid_ref_list(self):
        is_valid, error = validate_ref(["not", "valid"])
        assert is_valid is False
        assert "must be a string" in error

    def test_invalid_ref_empty(self):
        is_valid, error = validate_ref("")
        assert is_valid is False
        assert "cannot be empty" in error

    def test_invalid_ref_number(self):
        is_valid, error = validate_ref(123)
        assert is_valid is False
        assert "must be a string" in error


class TestFnSubValidation:
    def test_valid_sub_string(self):
        is_valid, error = validate_fn_sub("${AWS::StackName}-bucket")
        assert is_valid is True

    def test_valid_sub_list(self):
        is_valid, error = validate_fn_sub(["${Var}-value", {"Var": "test"}])
        assert is_valid is True

    def test_invalid_sub_number(self):
        is_valid, error = validate_fn_sub(123)
        assert is_valid is False
        assert "must be a string or list" in error

    def test_invalid_sub_list_wrong_length(self):
        is_valid, error = validate_fn_sub(["only-one"])
        assert is_valid is False
        assert "exactly 2 values" in error

    def test_invalid_sub_list_wrong_types(self):
        is_valid, error = validate_fn_sub([123, {"Var": "test"}])
        assert is_valid is False
        assert "template must be a string" in error


class TestFnGetAttValidation:
    def test_valid_getatt_list(self):
        is_valid, error = validate_fn_get_att(["MyResource", "Arn"])
        assert is_valid is True

    def test_valid_getatt_string(self):
        is_valid, error = validate_fn_get_att("MyResource.Arn")
        assert is_valid is True

    def test_invalid_getatt_string_no_dot(self):
        is_valid, error = validate_fn_get_att("NoDotHere")
        assert is_valid is False
        assert "must contain a dot" in error

    def test_invalid_getatt_list_wrong_length(self):
        is_valid, error = validate_fn_get_att(["OnlyOne"])
        assert is_valid is False
        assert "exactly 2 elements" in error

    def test_invalid_getatt_number(self):
        is_valid, error = validate_fn_get_att(123)
        assert is_valid is False
        assert "must be a string or list" in error


class TestFnJoinValidation:
    def test_valid_join(self):
        is_valid, error = validate_fn_join(["-", ["a", "b", "c"]])
        assert is_valid is True

    def test_valid_join_with_function(self):
        is_valid, error = validate_fn_join(["-", {"Ref": "MyList"}])
        assert is_valid is True

    def test_invalid_join_string(self):
        is_valid, error = validate_fn_join("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_join_wrong_length(self):
        is_valid, error = validate_fn_join(["-"])
        assert is_valid is False
        assert "exactly 2 values" in error

    def test_invalid_join_delimiter_not_string(self):
        is_valid, error = validate_fn_join([123, ["a", "b"]])
        assert is_valid is False
        assert "delimiter must be a string" in error


class TestFnIfValidation:
    def test_valid_if(self):
        is_valid, error = validate_fn_if(["MyCondition", "true-value", "false-value"])
        assert is_valid is True

    def test_invalid_if_string(self):
        is_valid, error = validate_fn_if("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_if_wrong_length(self):
        is_valid, error = validate_fn_if(["MyCondition", "true-value"])
        assert is_valid is False
        assert "exactly 3 values" in error


class TestFnSelectValidation:
    def test_valid_select(self):
        is_valid, error = validate_fn_select(["0", ["a", "b", "c"]])
        assert is_valid is True

    def test_invalid_select_string(self):
        is_valid, error = validate_fn_select("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_select_wrong_length(self):
        is_valid, error = validate_fn_select(["0"])
        assert is_valid is False
        assert "exactly 2 values" in error


class TestFnSplitValidation:
    def test_valid_split(self):
        is_valid, error = validate_fn_split([",", "a,b,c"])
        assert is_valid is True

    def test_invalid_split_string(self):
        is_valid, error = validate_fn_split("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_split_wrong_length(self):
        is_valid, error = validate_fn_split([","])
        assert is_valid is False
        assert "exactly 2 values" in error

    def test_invalid_split_delimiter_not_string(self):
        is_valid, error = validate_fn_split([123, "a,b,c"])
        assert is_valid is False
        assert "delimiter must be a string" in error


class TestFnAndValidation:
    def test_valid_and_two_conditions(self):
        is_valid, error = validate_fn_and([True, False])
        assert is_valid is True

    def test_valid_and_ten_conditions(self):
        is_valid, error = validate_fn_and([True] * 10)
        assert is_valid is True

    def test_invalid_and_string(self):
        is_valid, error = validate_fn_and("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_and_one_condition(self):
        is_valid, error = validate_fn_and([True])
        assert is_valid is False
        assert "2-10 conditions" in error

    def test_invalid_and_eleven_conditions(self):
        is_valid, error = validate_fn_and([True] * 11)
        assert is_valid is False
        assert "2-10 conditions" in error


class TestFnOrValidation:
    def test_valid_or_two_conditions(self):
        is_valid, error = validate_fn_or([True, False])
        assert is_valid is True

    def test_invalid_or_one_condition(self):
        is_valid, error = validate_fn_or([True])
        assert is_valid is False
        assert "2-10 conditions" in error


class TestFnNotValidation:
    def test_valid_not(self):
        is_valid, error = validate_fn_not([True])
        assert is_valid is True

    def test_invalid_not_string(self):
        is_valid, error = validate_fn_not("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_not_two_conditions(self):
        is_valid, error = validate_fn_not([True, False])
        assert is_valid is False
        assert "exactly 1 condition" in error


class TestFnEqualsValidation:
    def test_valid_equals(self):
        is_valid, error = validate_fn_equals(["a", "b"])
        assert is_valid is True

    def test_invalid_equals_string(self):
        is_valid, error = validate_fn_equals("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_equals_wrong_length(self):
        is_valid, error = validate_fn_equals(["only-one"])
        assert is_valid is False
        assert "exactly 2 values" in error


class TestFnFindInMapValidation:
    def test_valid_find_in_map(self):
        is_valid, error = validate_fn_find_in_map(["MapName", "TopKey", "SecondKey"])
        assert is_valid is True

    def test_invalid_find_in_map_string(self):
        is_valid, error = validate_fn_find_in_map("not-a-list")
        assert is_valid is False
        assert "must be a list" in error

    def test_invalid_find_in_map_wrong_length(self):
        is_valid, error = validate_fn_find_in_map(["MapName", "TopKey"])
        assert is_valid is False
        assert "exactly 3 values" in error


class TestFnBase64Validation:
    def test_valid_base64_string(self):
        is_valid, error = validate_fn_base64("Hello World")
        assert is_valid is True

    def test_valid_base64_with_function(self):
        is_valid, error = validate_fn_base64({"Ref": "MyParam"})
        assert is_valid is True

    def test_invalid_base64_number(self):
        is_valid, error = validate_fn_base64(123)
        assert is_valid is False
        assert "must be a string or function" in error


class TestFnGetAZsValidation:
    def test_valid_getazs_empty_string(self):
        is_valid, error = validate_fn_get_azs("")
        assert is_valid is True

    def test_valid_getazs_region(self):
        is_valid, error = validate_fn_get_azs("us-east-1")
        assert is_valid is True

    def test_valid_getazs_with_function(self):
        is_valid, error = validate_fn_get_azs({"Ref": "AWS::Region"})
        assert is_valid is True

    def test_invalid_getazs_number(self):
        is_valid, error = validate_fn_get_azs(123)
        assert is_valid is False
        assert "must be a string or function" in error


class TestFnImportValueValidation:
    def test_valid_import_value_string(self):
        is_valid, error = validate_fn_import_value("ExportedValue")
        assert is_valid is True

    def test_valid_import_value_with_function(self):
        is_valid, error = validate_fn_import_value({"Fn::Sub": "${AWS::StackName}-export"})
        assert is_valid is True

    def test_invalid_import_value_number(self):
        is_valid, error = validate_fn_import_value(123)
        assert is_valid is False
        assert "must be a string or function" in error


class TestConditionValidation:
    def test_valid_condition(self):
        is_valid, error = validate_condition("MyCondition")
        assert is_valid is True

    def test_invalid_condition_list(self):
        is_valid, error = validate_condition(["not", "valid"])
        assert is_valid is False
        assert "must be a string" in error

    def test_invalid_condition_empty(self):
        is_valid, error = validate_condition("")
        assert is_valid is False
        assert "cannot be empty" in error


class TestValidateIntrinsicFunction:
    def test_valid_ref(self):
        is_valid, error = validate_intrinsic_function({"Ref": "MyResource"})
        assert is_valid is True

    def test_valid_fn_sub(self):
        is_valid, error = validate_intrinsic_function({"Fn::Sub": "${AWS::StackName}"})
        assert is_valid is True

    def test_invalid_unknown_function(self):
        is_valid, error = validate_intrinsic_function({"Fn::Unknown": "value"})
        assert is_valid is False
        assert "Unknown intrinsic function" in error

    def test_invalid_multiple_keys(self):
        is_valid, error = validate_intrinsic_function({"Ref": "A", "Fn::Sub": "B"})
        assert is_valid is False
        assert "exactly 1 key" in error


class TestFunctionDictValidation:
    """Test that FunctionDict properly validates intrinsic functions."""

    def test_valid_ref_creates_function_dict(self):
        fd = FunctionDict(**{"Ref": "MyResource"})
        assert fd.Ref == "MyResource"

    def test_valid_fn_sub_creates_function_dict(self):
        fd = FunctionDict(**{"Fn::Sub": "${AWS::StackName}"})
        assert getattr(fd, "Fn::Sub") == "${AWS::StackName}"

    def test_invalid_ref_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FunctionDict(**{"Ref": ["invalid", "list"]})
        assert "Ref value must be a string" in str(exc_info.value)

    def test_invalid_fn_join_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FunctionDict(**{"Fn::Join": ["-"]})
        assert "exactly 2 values" in str(exc_info.value)

    def test_invalid_fn_if_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FunctionDict(**{"Fn::If": ["Cond", "TrueVal"]})
        assert "exactly 3 values" in str(exc_info.value)

    def test_invalid_fn_getatt_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FunctionDict(**{"Fn::GetAtt": "NoDotHere"})
        assert "must contain a dot" in str(exc_info.value)

    def test_invalid_fn_and_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FunctionDict(**{"Fn::And": [True]})
        assert "2-10 conditions" in str(exc_info.value)

    def test_invalid_fn_select_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FunctionDict(**{"Fn::Select": "not-a-list"})
        assert "must be a list" in str(exc_info.value)
