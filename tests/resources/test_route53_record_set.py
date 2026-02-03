import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.route53_record_set import Route53RecordSet


@pytest.fixture()
def valid_route53_record_set():
    return Route53RecordSet(
        **{
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
                "Name": "example.com.",
                "Type": "A",
                "HostedZoneId": "Z1234567890ABC",
                "TTL": "300",
                "ResourceRecords": ["192.0.2.1"],
            },
        }
    )


def test_valid_route53_record_set_resource(valid_route53_record_set):
    assert valid_route53_record_set.Properties.Name == "example.com."
    assert valid_route53_record_set.Properties.Type == "A"
    assert valid_route53_record_set.Properties.TTL == "300"
    assert valid_route53_record_set.Properties.ResourceRecords == ["192.0.2.1"]


def test_route53_record_set_cname():
    record = Route53RecordSet(
        **{
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
                "Name": "www.example.com.",
                "Type": "CNAME",
                "HostedZoneId": "Z1234567890ABC",
                "TTL": "300",
                "ResourceRecords": ["example.com"],
            },
        }
    )
    assert record.Properties.Type == "CNAME"


def test_route53_record_set_alias():
    record = Route53RecordSet(
        **{
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
                "Name": "example.com.",
                "Type": "A",
                "HostedZoneId": "Z1234567890ABC",
                "AliasTarget": {
                    "DNSName": "d111111abcdef8.cloudfront.net",
                    "HostedZoneId": "Z2FDTNDATAQYW2",
                    "EvaluateTargetHealth": False,
                },
            },
        }
    )
    assert record.Properties.AliasTarget.DNSName == "d111111abcdef8.cloudfront.net"
    assert record.Properties.AliasTarget.EvaluateTargetHealth is False


def test_route53_record_set_with_hosted_zone_name():
    record = Route53RecordSet(
        **{
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
                "Name": "www.example.com.",
                "Type": "A",
                "HostedZoneName": "example.com.",
                "TTL": "300",
                "ResourceRecords": ["192.0.2.1"],
            },
        }
    )
    assert record.Properties.HostedZoneName == "example.com."


def test_route53_record_set_geolocation():
    record = Route53RecordSet(
        **{
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
                "Name": "example.com.",
                "Type": "A",
                "HostedZoneId": "Z1234567890ABC",
                "TTL": "300",
                "ResourceRecords": ["192.0.2.1"],
                "SetIdentifier": "us-east-1",
                "GeoLocation": {
                    "ContinentCode": "NA",
                },
            },
        }
    )
    assert record.Properties.GeoLocation.ContinentCode == "NA"
    assert record.Properties.SetIdentifier == "us-east-1"


def test_route53_record_set_weighted():
    record = Route53RecordSet(
        **{
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
                "Name": "example.com.",
                "Type": "A",
                "HostedZoneId": "Z1234567890ABC",
                "TTL": "300",
                "ResourceRecords": ["192.0.2.1"],
                "SetIdentifier": "primary",
                "Weight": 70,
            },
        }
    )
    assert record.Properties.Weight == 70


def test_route53_record_set_failover():
    record = Route53RecordSet(
        **{
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
                "Name": "example.com.",
                "Type": "A",
                "HostedZoneId": "Z1234567890ABC",
                "TTL": "300",
                "ResourceRecords": ["192.0.2.1"],
                "SetIdentifier": "primary",
                "Failover": "PRIMARY",
                "HealthCheckId": "abc123",
            },
        }
    )
    assert record.Properties.Failover == "PRIMARY"
    assert record.Properties.HealthCheckId == "abc123"


def test_route53_record_set_requires_name():
    with pytest.raises(ValidationError):
        Route53RecordSet(
            **{
                "Type": "AWS::Route53::RecordSet",
                "Properties": {
                    "Type": "A",
                    "HostedZoneId": "Z1234567890ABC",
                },
            }
        )


def test_route53_record_set_requires_type():
    with pytest.raises(ValidationError):
        Route53RecordSet(
            **{
                "Type": "AWS::Route53::RecordSet",
                "Properties": {
                    "Name": "example.com.",
                    "HostedZoneId": "Z1234567890ABC",
                },
            }
        )
