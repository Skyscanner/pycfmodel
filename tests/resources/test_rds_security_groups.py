import pytest

from pycfmodel.model.resources.properties.security_group_ingress_prop import DBSecurityGroupIngressProp
from pycfmodel.model.resources.security_group import RDSDBSecurityGroup
from pycfmodel.model.resources.security_group_ingress import RDSDBSecurityGroupIngress


@pytest.mark.parametrize(
    "iprange, public",
    [
        ("10.0.0.0/8", False),
        ("0.0.0.0/8", False),
        ("0.0.0.0/0", True),
        ("192.168.0.1/24", False),
        ("172.128.16.2/8", True),
        ("1.2.3.4/32", True),
        ("1.2.3.4", True),
    ],
)
def test_rds_cidrip_is_public(iprange, public):
    assert DBSecurityGroupIngressProp(CIDRIP=iprange).is_public() == public


def test_rds_db_security_group_parsing():
    sg = RDSDBSecurityGroup(
        **{
            "Type": "AWS::RDS::DBSecurityGroup",
            "Properties": {
                "EC2VpcId": "vpc-id",
                "DBSecurityGroupIngress": [{"CIDRIP": "10.0.0.0/8"}],
                "GroupDescription": "Compliant RDS security group",
            },
        }
    )
    assert isinstance(sg, RDSDBSecurityGroup)


def test_rds_db_security_group_ingress_parsing():
    sg_ingress = RDSDBSecurityGroupIngress(
        **{
            "Type": "AWS::RDS::DBSecurityGroupIngress",
            "Properties": {"DBSecurityGroupName": "test-sg", "CIDRIP": "10.0.0.0/8"},
        }
    )
    assert isinstance(sg_ingress, RDSDBSecurityGroupIngress)
