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
def security_group_ingress_ipv4():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {"GroupId": "sg-12341234", "CidrIp": "", "FromPort": 46, "ToPort": 46, "IpProtocol": "tcp"},
        }
    )


@pytest.fixture()
def security_group_ingress_ipv6():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {"GroupId": "sg-12341234", "CidrIpv6": "", "FromPort": 46, "ToPort": 46, "IpProtocol": "tcp"},
        }
    )


def test_security_group_ingress(security_group_ingress_ipv4):
    assert security_group_ingress_ipv4.Properties.GroupId == "sg-12341234"
    assert isinstance(security_group_ingress_ipv4.Properties.FromPort, int)


@pytest.mark.parametrize("ipv4, expected", [("1.1.1.1/0", True), (None, False), (1, False), ("172.16.0.0/12", False)])
def test_slash_zero4(ipv4, expected, security_group_ingress_ipv4):
    security_group_ingress_ipv4.Properties.CidrIp = ipv4
    assert security_group_ingress_ipv4.ipv4_slash_zero() == expected


@pytest.mark.parametrize("ipv6, expected", [("1.1.1.1/0", True), (None, False), (1, False), ("172.16.0.0/12", False)])
def test_slash_zero6(ipv6, expected, security_group_ingress_ipv6):
    security_group_ingress_ipv6.Properties.CidrIpv6 = ipv6
    assert security_group_ingress_ipv6.ipv6_slash_zero() == expected


@pytest.mark.parametrize(
    "ipv4, expected", [("1.1.1.1/0", False), ("10.0.0.0/8", True), (None, False), (1, False), ("172.0.0.0/8", False)]
)
def test_ipv4_private_addr(ipv4, expected, security_group_ingress_ipv4):
    security_group_ingress_ipv4.Properties.CidrIp = ipv4
    assert security_group_ingress_ipv4.ipv4_private_addr() == expected


@pytest.mark.parametrize(
    "ipv6, expected",
    [
        ("1.1.1.1/0", False),
        ("fc00::/7", True),
        ("FD00::/8", True),
        (None, False),
        (1, False),
        ("0001:0db8:85a3:0000:0000:8a2e:0370:7334", False),
    ],
)
def test_ipv6_private_addr(ipv6, expected, security_group_ingress_ipv6):
    security_group_ingress_ipv6.Properties.CidrIpv6 = ipv6
    assert security_group_ingress_ipv6.ipv6_private_addr() == expected
