import pytest

from pycfmodel.model.resources.security_group_ingress import SecurityGroupIngress


@pytest.fixture()
def security_group_ingress_ipv4_1():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIp": "1.1.1.1/0",
                "FromPort": 46,
                "ToPort": 46,
                "IpProtocol": "tcp",
            },
        }
    )


@pytest.fixture()
def security_group_ingress_ipv4_2():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {
                "GroupId": "sg-2345",
                "CidrIp": "127.0.0.0",
                "FromPort": 46,
                "ToPort": 46,
                "IpProtocol": "tcp",
            },
        }
    )


@pytest.fixture()
def security_group_ingress_ipv6():
    return SecurityGroupIngress(
        **{
            "Type": "AWS::EC2::SecurityGroupIngress",
            "Properties": {
                "GroupId": "sg-12341234",
                "CidrIpv6": "2001:0db8:0000:0000:0000:ff00:0042:8329",
                "FromPort": 46,
                "ToPort": 46,
                "IpProtocol": "tcp",
            },
        }
    )


def test_security_group_ingress(security_group_ingress_ipv4_1):
    assert security_group_ingress_ipv4_1.Properties.GroupId == "sg-12341234"
    assert isinstance(security_group_ingress_ipv4_1.Properties.FromPort, int)


def test_slash_zero4(security_group_ingress_ipv4_1):
    assert security_group_ingress_ipv4_1.ipv4_slash_zero() == True


def test_not_slash_zero4(security_group_ingress_ipv4_2):
    assert security_group_ingress_ipv4_2.ipv4_slash_zero() == False


def test_not_slash_zero6(security_group_ingress_ipv6):
    assert security_group_ingress_ipv6.ipv6_slash_zero() == False
