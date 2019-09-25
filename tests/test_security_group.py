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
from pycfmodel.model.resources.security_group import SecurityGroup

sg1 = {
    "sg": {
        "Type": "AWS::EC2::SecurityGroup",
        "Properties": {
            "GroupDescription": "some_group_desc",
            "SecurityGroupIngress": {"CidrIp": "10.1.2.3/32", "FromPort": 34, "ToPort": 36, "IpProtocol": "tcp"},
            "SecurityGroupEgress": {"CidrIp": "10.1.2.3/32", "FromPort": 34, "ToPort": 36, "IpProtocol": "tcp"},
            "VpcId": "vpc-9f8e9dfa",
        },
    }
}

sg_obj = SecurityGroup("sg", sg1["sg"])


def test_main():
    assert sg_obj.group_description == "some_group_desc"
    assert not sg_obj.security_group_ingress[0].ipv4_slash_zero()
    assert not sg_obj.security_group_egress[0].ipv4_slash_zero()
