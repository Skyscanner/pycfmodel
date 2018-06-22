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


class SecurityGroupIngressProp(object):

    def __init__(self, ingress):
        """
        "CidrIp" : String,
        "CidrIpv6" : String,
        "Description" : String,
        "FromPort" : Integer,
        "IpProtocol" : String,
        "SourceSecurityGroupId" : String,
        "SourceSecurityGroupName" : String,
        "SourceSecurityGroupOwnerId" : String,
        "ToPort" : Integer
        """
        self.cidr_ip = ingress.get("CidrIp")
        self.cidr_ipv6 = ingress.get("CidrIpv6")
        self.description = ingress.get("Description")
        self.from_port = ingress.get("FromPort")
        self.ip_protocol = ingress.get("IpProtocol")
        self.source_security_group_id = ingress.get("SourceSecurityGroupId")
        self.source_security_group_name = ingress.get("SourceSecurityGroupName")
        self.source_security_group_owner_id = ingress.get("SourceSecurityGroupOwnerId")
        self.to_port = ingress.get("ToPort")

    def ipv4_slash_zero(self):
        if not self.cidr_ip or not isinstance(self.cidr_ip, str):
            return False
        return self.cidr_ip.endswith('/0')

    def ipv6_slash_zero(self):
        if not self.cidr_ipv6 or not isinstance(self.cidr_ipv6, str):
            return False
        return self.cidr_ipv6.endswith('/0')
