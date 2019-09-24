"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from pycfmodel.model.intrinsic_function_resolver import IntrinsicFunctionResolver


def test_ref_and_import_value():
    computed_parameters = {"abc": "ABC"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Ref": "abc"}
    assert intrinsic_function_resolver.resolve(function) == "ABC"

    function = {"Fn::ImportValue": "abc"}
    assert intrinsic_function_resolver.resolve(function) == "ABC"


def test_join():
    computed_parameters = {}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Join": ["", ["arn:", "aws", ":s3:::elasticbeanstalk-*-", "1234567890"]]}
    assert intrinsic_function_resolver.resolve(function) == "arn:aws:s3:::elasticbeanstalk-*-1234567890"


def test_find_in_map():
    computed_parameters = {}
    mappings = {"RegionMap": {"us-east-1": {"HVM64": "ami-0ff8a91507f77f867"}}}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::FindInMap": ["RegionMap", "us-east-1", "HVM64"]}
    assert intrinsic_function_resolver.resolve(function) == "ami-0ff8a91507f77f867"


def test_sub():
    computed_parameters = {}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Sub": ["www.${Domain}", {"Domain": "skyscanner.net"}]}
    assert intrinsic_function_resolver.resolve(function) == "www.skyscanner.net"


def test_select():
    computed_parameters = {"DbSubnetIpBlocks": ["10.0.48.0/24", "10.0.112.0/24", "10.0.176.0/24"]}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Select": ["1", ["apples", "grapes", "oranges", "mangoes"]]}
    assert intrinsic_function_resolver.resolve(function) == "grapes"


def test_split():
    computed_parameters = {}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Split": ["|", "a||c|"]}
    assert intrinsic_function_resolver.resolve(function) == ["a", "", "c", ""]


def test_and():
    computed_parameters = {"EnvironmentType": "prod", "ASecurityGroup": "sg-mysggroup"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {
        "Fn::And": [
            {"Fn::Equals": ["sg-mysggroup", {"Ref": "ASecurityGroup"}]},
            {"Fn::Equals": [{"Ref": "EnvironmentType"}, "prod"]},
        ]
    }

    assert intrinsic_function_resolver.resolve(function) == True


def test_or():
    computed_parameters = {"EnvironmentType": "prod", "ASecurityGroup": "sg-othersggroup"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {
        "Fn::Or": [
            {"Fn::Equals": ["sg-mysggroup", {"Ref": "ASecurityGroup"}]},
            {"Fn::Equals": [{"Ref": "EnvironmentType"}, "prod"]},
        ]
    }

    assert intrinsic_function_resolver.resolve(function) == True


def test_not():
    computed_parameters = {"EnvironmentType": "prod"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Not": [{"Fn::Equals": [{"Ref": "EnvironmentType"}, "prod"]}]}

    assert intrinsic_function_resolver.resolve(function) == False


def test_equals():
    computed_parameters = {"EnvironmentType": "prod"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Equals": [{"Ref": "EnvironmentType"}, "prod"]}

    assert intrinsic_function_resolver.resolve(function) == True


def test_base64():
    computed_parameters = {}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Base64": "holap :)"}
    assert intrinsic_function_resolver.resolve(function) == "aG9sYXAgOik="


def test_empty_sub():
    computed_parameters = {}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Sub": "www.skyscanner.net"}
    assert intrinsic_function_resolver.resolve(function) == "www.skyscanner.net"


def test_select_and_ref():
    computed_parameters = {"DbSubnetIpBlocks": ["10.0.48.0/24", "10.0.112.0/24", "10.0.176.0/24"]}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Select": ["0", {"Ref": "DbSubnetIpBlocks"}]}
    assert intrinsic_function_resolver.resolve(function) == "10.0.48.0/24"


def test_join_and_ref():
    computed_parameters = {"Partition": "patata", "AWS::AccountId": "1234567890"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {
        "Fn::Join": ["", ["arn:", {"Ref": "Partition"}, ":s3:::elasticbeanstalk-*-", {"Ref": "AWS::AccountId"}]]
    }
    assert intrinsic_function_resolver.resolve(function) == "arn:patata:s3:::elasticbeanstalk-*-1234567890"


def test_sub_and_ref():
    computed_parameters = {"RootDomainName": "skyscanner.net"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Sub": ["www.${Domain}", {"Domain": {"Ref": "RootDomainName"}}]}
    assert intrinsic_function_resolver.resolve(function) == "www.skyscanner.net"


def test_select_and_split():
    computed_parameters = {"AccountSubnetIDs": "id1,id2,id3"}
    mappings = {}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::Select": ["2", {"Fn::Split": [",", {"Ref": "AccountSubnetIDs"}]}]}
    assert intrinsic_function_resolver.resolve(function) == "id3"


def test_find_in_map_and_ref():
    computed_parameters = {"AWS::Region": "us-east-1"}
    mappings = {"RegionMap": {"us-east-1": {"HVM64": "ami-0ff8a91507f77f867"}}}
    intrinsic_function_resolver = IntrinsicFunctionResolver(computed_parameters, mappings)

    function = {"Fn::FindInMap": ["RegionMap", {"Ref": "AWS::Region"}, "HVM64"]}
    assert intrinsic_function_resolver.resolve(function) == "ami-0ff8a91507f77f867"
