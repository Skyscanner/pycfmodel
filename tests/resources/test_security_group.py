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

from pycfmodel.model.resources.security_group import SecurityGroup


@pytest.fixture()
def security_group():
    return SecurityGroup(
        **{
            "Type": "AWS::EC2::SecurityGroup",
            "Properties": {
                "GroupDescription": "some_group_desc",
                "SecurityGroupIngress": [{"CidrIp": "10.1.2.3/32", "FromPort": 34, "ToPort": 36, "IpProtocol": "tcp"}],
                "SecurityGroupEgress": [{"CidrIp": "10.1.2.3/32", "FromPort": 34, "ToPort": 36, "IpProtocol": "tcp"}],
                "VpcId": "vpc-9f8e9dfa",
            },
        }
    )


def test_security_group(security_group):
    assert security_group.Properties.GroupDescription == "some_group_desc"
    assert not security_group.Properties.SecurityGroupIngress[0].ipv4_slash_zero()
    assert not security_group.Properties.SecurityGroupEgress[0].ipv4_slash_zero()
