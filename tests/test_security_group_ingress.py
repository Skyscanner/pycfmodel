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
from pycfmodel.model.resources.security_group_ingress import SecurityGroupIngress

sg_ingress = {
    "securityGroupIngress": {
        "Type": "AWS::EC2::SecurityGroupIngress",
        "Properties": {
            "GroupId": "sg-12341234",
            "CidrIp": "0.0.0.0/0",
            "FromPort": 46,
            "ToPort": 46,
            "IpProtocol": "tcp"
        }
    }
}
sg_ingress2 = {
    "securityGroupIngress2": {
        "Type": "AWS::EC2::SecurityGroupIngress",
        "Properties": {
            "GroupId": "sg-12341234",
            "CidrIpv6": "2001:0db8:0000:0000:0000:ff00:0042:8329/0",
            "FromPort": 46,
            "ToPort": 46,
            "IpProtocol": "tcp"
        }
    }
}

sg_ingres_obj = SecurityGroupIngress(
    "securityGroupIngress",
    sg_ingress["securityGroupIngress"],
)
sg_ingres_obj2 = SecurityGroupIngress(
    "securityGroupIngress2",
    sg_ingress2["securityGroupIngress2"],
)


def test_main():
    assert sg_ingres_obj.group_id == "sg-12341234"
    assert isinstance(sg_ingres_obj.from_port, int)


def test_slash_zero4():
    assert sg_ingres_obj.ipv4_slash_zero()
    assert not sg_ingres_obj2.ipv4_slash_zero()


def test_slash_zero6():
    assert not sg_ingres_obj.ipv6_slash_zero()
    assert sg_ingres_obj2.ipv6_slash_zero()
