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

from pycfmodel.model.resources.security_group_ingress import SecurityGroupIngress


@pytest.fixture()
def security_group_ingress_ipv4_1():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {"GroupId": "sg-1", "CidrIp": "0.0.0.0/0", "FromPort": 46, "ToPort": 46, "IpProtocol": "tcp"},
        }
    )


@pytest.fixture()
def security_group_ingress_ipv4_2():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {"GroupId": "sg-2", "CidrIp": "127.0.0.0", "FromPort": 46, "ToPort": 46, "IpProtocol": "tcp"},
        }
    )


@pytest.fixture()
def security_group_ingress_ipv6_1():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIpv6": "fc00::/7",
                "FromPort": 46,
                "ToPort": 46,
                "IpProtocol": "tcp",
            },
        }
    )


def test_security_group_ingress(security_group_ingress_ipv4_1):
    assert security_group_ingress_ipv4_1.Properties.GroupId == "sg-1"
    assert isinstance(security_group_ingress_ipv4_1.Properties.FromPort, int)


def test_slash_zero4(security_group_ingress_ipv4_1):
    assert security_group_ingress_ipv4_1.ipv4_slash_zero() == True


def test_not_slash_zero4(security_group_ingress_ipv4_2):
    assert security_group_ingress_ipv4_2.ipv4_slash_zero() == False


def test_not_slash_zero6(security_group_ingress_ipv6_1):
    assert security_group_ingress_ipv6_1.ipv6_slash_zero() == False
