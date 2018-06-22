"""
Copyright 2018 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from pycfmodel.model.resources.security_group_egress import SecurityGroupEgress

sg_egress = {
    "securityGroupEgress": {
        "Type": "AWS::EC2::SecurityGroupEgress",
        "Properties": {
            "GroupId": "sg-12341234",
            "CidrIp": "1.1.1.1/0",
            "FromPort": 41,
            "ToPort": 45,
            "IpProtocol": "tcp"
        }
    }
}
sg_egress2 = {
    "securityGroupEgress2": {
        "Type": "AWS::EC2::SecurityGroupEgress",
        "Properties": {
            "GroupId": "sg-12341234",
            "CidrIpv6": "1.1.1.1/0",
            "FromPort": 41,
            "ToPort": 45,
            "IpProtocol": "tcp"
        }
    }
}

sg_egress_obj1 = SecurityGroupEgress(
    "securityGroupEgress",
    sg_egress["securityGroupEgress"],
)
sg_egress_obj2 = SecurityGroupEgress(
    "securityGroupEgress2",
    sg_egress2["securityGroupEgress2"],
)


def test_main():
    assert sg_egress_obj1.group_id == "sg-12341234"
    assert isinstance(sg_egress_obj1.from_port, int)


def test_slash_zero4():
    assert sg_egress_obj1.ipv4_slash_zero()
    assert not sg_egress_obj2.ipv4_slash_zero()


def test_slash_zero6():
    assert not sg_egress_obj1.ipv6_slash_zero()
    assert sg_egress_obj2.ipv6_slash_zero()
