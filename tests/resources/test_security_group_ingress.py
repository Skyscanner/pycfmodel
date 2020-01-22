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
def security_group_ingress_1():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIp": "0.0.0.0/0",
                "FromPort": 46,
                "ToPort": 46,
                "IpProtocol": "tcp",
            },
        }
    )


@pytest.fixture()
def security_group_ingress_2():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIpv6": "2001:0db8:0000:0000:0000:ff00:0042:8329/0",
                "FromPort": 46,
                "ToPort": 46,
                "IpProtocol": "tcp",
            },
        }
    )


def test_security_group_ingress(security_group_ingress_1):
    assert security_group_ingress_1.Properties.GroupId == "sg-12341234"
    assert isinstance(security_group_ingress_1.Properties.FromPort, int)


def test_slash_zero4(security_group_ingress_1, security_group_ingress_2):
    assert security_group_ingress_1.ipv4_slash_zero()
    assert not security_group_ingress_2.ipv4_slash_zero()


def test_slash_zero6(security_group_ingress_1, security_group_ingress_2):
    assert not security_group_ingress_1.ipv6_slash_zero()
    assert security_group_ingress_2.ipv6_slash_zero()
