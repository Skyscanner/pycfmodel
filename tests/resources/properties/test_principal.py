import pytest
from pydantic import ValidationError

from pycfmodel.model.resources.properties.statement import Principal


@pytest.mark.parametrize(
    "principal",
    [
        {"AWS": "*"},
        {"AWS": "123456789012"},
        {"AWS": "arn:aws:iam::123456789012:root"},
        {"AWS": "arn:aws:iam::123456789012:role/role-name"},
        {"AWS": "arn:aws:sts::123456789012:federated-user/user-name"},
        {"AWS": ["123456789012", "555555555555"]},
        {"AWS": ["arn:aws:iam::123456789012:user/user-name-1", "arn:aws:iam::123456789012:user/user-name-2"]},
        {"CanonicalUser": "79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be"},
        {
            "AWS": ["arn:aws:iam::123456789012:root", "999999999999"],
            "CanonicalUser": "79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be",
        },
        {"Federated": "cognito-identity.amazonaws.com"},
        {"Federated": "arn:aws:iam::123456789012:saml-provider/provider-name"},
        {"Service": ["ecs.amazonaws.com", "elasticloadbalancing.amazonaws.com"]},
    ],
)
def test_principal(principal):
    try:
        Principal.model_validate(principal)
    except ValidationError as exc:
        assert False, f"{principal} raised an exception {exc}"
