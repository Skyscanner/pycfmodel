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


class SecurityGroupEgressProp(object):

    def __init__(self, egress):
        """
        "CidrIp" : String,
        "CidrIpv6" : String,
        "Description" : String,
        "DestinationPrefixListId" : String,
        "DestinationSecurityGroupId" : String,
        "FromPort" : Integer,
        "IpProtocol" : String,
        "ToPort" : Integer
        """
        self.cidr_ip = egress.get("cidr_ip")
        self.cidr_ipv6 = egress.get("cidr_ipv6")
        self.description = egress.get("description")
        self.destination_prefix_list_id = egress.get("destination_prefix_list_id")
        self.destination_security_group_id = egress.get("destination_security_group_id")
        self.from_port = egress.get("from_port")
        self.ip_protocol = egress.get("ip_protocol")
        self.to_port = egress.get("to_port")

    def ipv4_slash_zero(self):
        if not self.cidr_ip or not isinstance(self.cidr_ip, str):
            return False
        return self.cidr_ip.endswith('/0')

    def ipv6_slash_zero(self):
        if not self.cidr_ipv6 or not isinstance(self.cidr_ipv6, str):
            return False
        return self.cidr_ipv6.endswith('/0')
