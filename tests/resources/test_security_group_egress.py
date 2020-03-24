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
import pytest

from pycfmodel.model.resources.security_group_egress import SecurityGroupEgress


@pytest.fixture()
def security_group_egress_ipv4_1():
    return SecurityGroupEgress(
        **{
            "Type": "AWS::EC2::SecurityGroupEgress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIp": "1.1.1.1/0",
                "FromPort": 41,
                "ToPort": 45,
                "IpProtocol": "tcp",
            },
        }
    )


@pytest.fixture()
def security_group_egress_ipv4_2():
    return SecurityGroupEgress(
        **{
            "Type": "AWS::EC2::SecurityGroupEgress",
            "Properties": {
                "GroupId": "sg-2345",
                "CidrIp": "172.0.0.0",
                "FromPort": 41,
                "ToPort": 45,
                "IpProtocol": "tcp",
            },
        }
    )


@pytest.fixture()
def security_group_egress_ipv6():
    return SecurityGroupEgress(
        **{
            "Type": "AWS::EC2::SecurityGroupEgress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIpv6": "fc00::/7",
                "FromPort": 41,
                "ToPort": 45,
                "IpProtocol": "tcp",
            },
        }
    )


def test_security_group_egress(security_group_egress_ipv4_1):
    assert security_group_egress_ipv4_1.Properties.GroupId == "sg-12341234"
    assert isinstance(security_group_egress_ipv4_1.Properties.FromPort, int)


def test_slash_zero4(security_group_egress_ipv4_1):
    assert security_group_egress_ipv4_1.ipv4_slash_zero() == True


def test_not_slash_zero4(security_group_egress_ipv4_2):
    assert security_group_egress_ipv4_2.ipv4_slash_zero() == False


def test_not_slash_zero6(security_group_egress_ipv6):
    assert security_group_egress_ipv6.ipv6_slash_zero() == False
