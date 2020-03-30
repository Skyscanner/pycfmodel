import re

AWS_NOVALUE = "AWS::NoValue"

IMPLEMENTED_FUNCTIONS = {
    "Condition",
    "Fn::And",
    "Fn::Base64",
    "Fn::Equals",
    "Fn::FindInMap",
    "Fn::GetAtt",
    "Fn::GetAZs",
    "Fn::If",
    "Fn::ImportValue",
    "Fn::Join",
    "Fn::Not",
    "Fn::Or",
    "Fn::Select",
    "Fn::Split",
    "Fn::Sub",
    "Ref",
}

CONDITION_MODIFIERS = {"ForAllValues", "ForAnyValue", "IfExists"}

CONDITION_FUNCTIONS = {
    "ArnEquals",
    "ArnLike",
    "ArnNotEquals",
    "ArnNotLike",
    "Bool",
    "DateEquals",
    "DateGreaterThan",
    "DateGreaterThanEquals",
    "DateLessThan",
    "DateLessThanEquals",
    "DateNotEquals",
    "IpAddress",
    "Null",
    "NotIpAddress",
    "NumericEquals",
    "NumericNotEquals",
    "NumericLessThan",
    "NumericLessThanEquals",
    "NumericGreaterThan",
    "NumericGreaterThanEquals",
    "StringEquals",
    "StringLike",
    "StringNotEquals",
    "StringEqualsIgnoreCase",
    "StringNotEqualsIgnoreCase",
    "StringLike",
    "StringNotLike",
}

CONTAINS_STAR = re.compile(r"^.*[*].*$")
CONTAINS_CF_PARAM = re.compile(r"(\$\{[\w\:]+\})")

IPV4_ZERO_VALUE = "0.0.0.0/0"
IPV6_ZERO_VALUE = "::/0"
