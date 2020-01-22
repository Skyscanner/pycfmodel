"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
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
