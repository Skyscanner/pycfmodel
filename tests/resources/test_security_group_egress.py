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
def security_group_egress_1():
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
def security_group_egress_2():
    return SecurityGroupEgress(
        **{
            "Type": "AWS::EC2::SecurityGroupEgress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIpv6": "1.1.1.1/0",
                "FromPort": 41,
                "ToPort": 45,
                "IpProtocol": "tcp",
            },
        }
    )


def test_security_group_egress(security_group_egress_1):
    assert security_group_egress_1.Properties.GroupId == "sg-12341234"
    assert isinstance(security_group_egress_1.Properties.FromPort, int)


def test_slash_zero4(security_group_egress_1, security_group_egress_2):
    assert security_group_egress_1.ipv4_slash_zero()
    assert not security_group_egress_2.ipv4_slash_zero()


def test_slash_zero6(security_group_egress_1, security_group_egress_2):
    assert not security_group_egress_1.ipv6_slash_zero()
    assert security_group_egress_2.ipv6_slash_zero()
