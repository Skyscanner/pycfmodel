from ipaddress import IPv4Network

from pycfmodel.model.resources.wafv2_ip_set import WAFv2IPSet, WAFv2IPSetProperties


def test_wafv2_ipset_with_large_cidr():
    """Test that WAFv2::IPSet can handle large CIDR ranges like /8 without hanging."""
    resource_dict = {
        "Type": "AWS::WAFv2::IPSet",
        "Properties": {
            "Addresses": [
                "17.0.0.0/8",  # Large /8 CIDR (16M+ addresses)
                "192.168.1.0/24",
                "10.0.0.0/16",
            ],
            "Description": "Test IP set with large CIDR",
            "IPAddressVersion": "IPV4",
            "Scope": "CLOUDFRONT",
        },
    }

    resource = WAFv2IPSet(**resource_dict)

    assert resource.Type == "AWS::WAFv2::IPSet"
    assert isinstance(resource.Properties, WAFv2IPSetProperties)
    assert len(resource.Properties.Addresses) == 3
    assert resource.Properties.Addresses[0] == IPv4Network("17.0.0.0/8")
    assert isinstance(resource.Properties.Addresses[0], IPv4Network)
    assert resource.Properties.IPAddressVersion == "IPV4"
    assert resource.Properties.Scope == "CLOUDFRONT"


def test_wafv2_ipset_with_ipv6():
    """Test WAFv2::IPSet with IPv6 addresses."""
    resource_dict = {
        "Type": "AWS::WAFv2::IPSet",
        "Properties": {
            "Addresses": [
                "0000:0000:0000:0000:0000:0000:0000:0000/1",
                "8000:0000:0000:0000:0000:0000:0000:0000/1",
            ],
            "Description": "IPv6 ALL range",
            "IPAddressVersion": "IPV6",
            "Scope": "CLOUDFRONT",
        },
    }

    resource = WAFv2IPSet(**resource_dict)

    assert resource.Type == "AWS::WAFv2::IPSet"
    assert len(resource.Properties.Addresses) == 2
    assert resource.Properties.IPAddressVersion == "IPV6"


def test_wafv2_ipset_with_tags():
    """Test WAFv2::IPSet with tags."""
    resource_dict = {
        "Type": "AWS::WAFv2::IPSet",
        "Properties": {
            "Addresses": ["192.168.1.0/24"],
            "Description": "Test IP set",
            "IPAddressVersion": "IPV4",
            "Name": "TestIPSet",
            "Scope": "REGIONAL",
            "Tags": [
                {"Key": "Environment", "Value": "Production"},
                {"Key": "Project", "Value": "Security"},
            ],
        },
    }

    resource = WAFv2IPSet(**resource_dict)

    assert resource.Type == "AWS::WAFv2::IPSet"
    assert resource.Properties.Name == "TestIPSet"
    assert resource.Properties.Scope == "REGIONAL"
    assert len(resource.Properties.Tags) == 2
    assert resource.Properties.Tags[0].Key == "Environment"


def test_wafv2_ipset_with_invalid_ip():
    """Test that WAFv2::IPSet fails validation when given an invalid IP address."""
    import pytest
    from pydantic import ValidationError

    resource_dict = {
        "Type": "AWS::WAFv2::IPSet",
        "Properties": {
            "Addresses": ["not.a.valid.ip"],
            "IPAddressVersion": "IPV4",
            "Scope": "CLOUDFRONT",
        },
    }

    with pytest.raises(ValidationError):
        WAFv2IPSet(**resource_dict)
