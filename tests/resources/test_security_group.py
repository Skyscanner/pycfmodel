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
