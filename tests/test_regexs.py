import pytest

from pycfmodel.constants import CONTAINS_CF_PARAM, CONTAINS_STAR


@pytest.mark.parametrize(
    "string, expected",
    [
        ("*", True),
        ("*abc", True),
        ("abc*", True),
        ("abc*def", True),
        ("abc*def*ghi", True),
        ("*abc*def*ghi*", True),
        ("abcdef", False),
    ],
)
def test_contains_star(string, expected):
    assert bool(CONTAINS_STAR.match(string)) == expected


@pytest.mark.parametrize(
    "string, expected",
    [
        ("abcdef", []),
        ("abc${param}def", ["${param}"]),
        ("abc${Ref::abc}def", ["${Ref::abc}"]),
        ("abc${Ref::abc123}def", ["${Ref::abc123}"]),
    ],
)
def test_contains_cf_param(string, expected):
    assert CONTAINS_CF_PARAM.findall(string) == expected
