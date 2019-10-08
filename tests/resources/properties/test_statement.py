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
import re
import pytest

from pycfmodel.model.resources.properties.statement import Statement


@pytest.fixture()
def statement_1():
    return Statement(**{"Effect": "Allow", "Action": ["action1"], "NotAction": "action2", "Resource": ["arn"]})


@pytest.fixture()
def statement_2():
    return Statement(**{"Effect": "Allow", "Action": "action1", "NotAction": ["action2"], "Resource": ["arn"]})


@pytest.fixture()
def statement_3():
    return Statement(**{"Effect": "Allow", "Action": "action1", "Resource": ["arn1"], "NotResource": "arn2"})


@pytest.fixture()
def statement_4():
    return Statement(**{"Effect": "Allow", "Action": "action2", "Resource": "arn1", "NotResource": ["arn2"]})


@pytest.fixture()
def statement_principal_1():
    return Statement(**{"Principal": {"AWS": "arn:aws:iam::123456789012:root"}})


@pytest.fixture()
def statement_principal_2():
    return Statement(
        **{
            "Principal": {
                "AWS": ["arn:aws:iam::AWS-account-ID:user/user-name-1", "arn:aws:iam::AWS-account-ID:user/UserName2"]
            }
        }
    )


@pytest.fixture()
def statement_principal_3():
    return Statement(**{"Principal": {"Federated": "cognito-identity.amazonaws.com"}})


@pytest.fixture()
def statement_principal_4():
    return Statement(**{"Principal": "arn:aws:iam::123456789012:root"})


@pytest.fixture()
def statement_principal_5():
    return Statement(
        **{"Principal": ["arn:aws:iam::AWS-account-ID:user/user-name-1", "arn:aws:iam::AWS-account-ID:user/UserName2"]}
    )


@pytest.fixture()
def statement_not_principal_1():
    return Statement(**{"NotPrincipal": {"AWS": "arn:aws:iam::123456789012:root"}})


@pytest.fixture()
def statement_not_principal_2():
    return Statement(
        **{
            "NotPrincipal": {
                "AWS": ["arn:aws:iam::AWS-account-ID:user/user-name-1", "arn:aws:iam::AWS-account-ID:user/UserName2"]
            }
        }
    )


@pytest.fixture()
def statement_not_principal_3():
    return Statement(**{"NotPrincipal": {"Federated": "cognito-identity.amazonaws.com"}})


@pytest.fixture()
def statement_not_principal_4():
    return Statement(**{"NotPrincipal": "arn:aws:iam::123456789012:root"})


@pytest.fixture()
def statement_not_principal_5():
    return Statement(
        **{
            "NotPrincipal": [
                "arn:aws:iam::AWS-account-ID:user/user-name-1",
                "arn:aws:iam::AWS-account-ID:user/UserName2",
            ]
        }
    )


@pytest.mark.parametrize(
    "statement, expected_output",
    [
        (statement_1(), ["action1", "action2"]),
        (statement_2(), ["action1", "action2"]),
        (statement_3(), ["action1"]),
        (statement_4(), ["action2"]),
    ],
)
def test_get_action_list(statement, expected_output):
    assert statement.get_action_list() == expected_output


@pytest.mark.parametrize(
    "statement, expected_output",
    [
        (statement_1(), ["arn"]),
        (statement_2(), ["arn"]),
        (statement_3(), ["arn1", "arn2"]),
        (statement_4(), ["arn1", "arn2"]),
    ],
)
def test_get_resource_list(statement, expected_output):
    assert statement.get_resource_list() == expected_output


@pytest.mark.parametrize(
    "statement, expected_output",
    [
        (statement_principal_1(), ["arn:aws:iam::123456789012:root"]),
        (
            statement_principal_2(),
            ["arn:aws:iam::AWS-account-ID:user/user-name-1", "arn:aws:iam::AWS-account-ID:user/UserName2"],
        ),
        (statement_principal_3(), ["cognito-identity.amazonaws.com"]),
        (statement_principal_4(), ["arn:aws:iam::123456789012:root"]),
        (
            statement_principal_5(),
            ["arn:aws:iam::AWS-account-ID:user/user-name-1", "arn:aws:iam::AWS-account-ID:user/UserName2"],
        ),
        (statement_not_principal_1(), ["arn:aws:iam::123456789012:root"]),
        (
            statement_not_principal_2(),
            ["arn:aws:iam::AWS-account-ID:user/user-name-1", "arn:aws:iam::AWS-account-ID:user/UserName2"],
        ),
        (statement_not_principal_3(), ["cognito-identity.amazonaws.com"]),
        (statement_not_principal_4(), ["arn:aws:iam::123456789012:root"]),
        (
            statement_not_principal_5(),
            ["arn:aws:iam::AWS-account-ID:user/user-name-1", "arn:aws:iam::AWS-account-ID:user/UserName2"],
        ),
    ],
)
def test_get_principal_list(statement, expected_output):
    assert statement.get_principal_list() == expected_output


#
# @pytest.mark.parametrize(
#     "statement, pattern, expected_output",
#     [
#         (statement_1(), re.compile(r"^$"), ["arn"]),
#         (statement_2(), re.compile(r"^$"), ["arn"]),
#         (statement_3(), re.compile(r"^$"), ["arn1", "arn2"]),
#         (statement_4(), re.compile(r"^$"), ["arn1", "arn2"]),
#     ],
# )
# def test_actions_with(statement, pattern, expected_output):
#     assert statement.actions_with(pattern) == expected_output


@pytest.mark.parametrize(
    "statement, pattern, expected_output",
    [
        (statement_principal_1(), re.compile(r"^.*123456789012.*$"), ["arn:aws:iam::123456789012:root"]),
        (statement_principal_2(), re.compile(r"^.*user-name-1$"), ["arn:aws:iam::AWS-account-ID:user/user-name-1"]),
        (statement_principal_3(), re.compile(r"^.*\.amazonaws\.com$"), ["cognito-identity.amazonaws.com"]),
    ],
)
def test_principals_with(statement, pattern, expected_output):
    print(statement.principals_with(pattern))
    assert statement.principals_with(pattern) == expected_output


@pytest.mark.parametrize(
    "statement, pattern, expected_output",
    [
        (statement_1(), re.compile(r"^[a]+$"), []),
        (statement_2(), re.compile(r"^[arn]+$"), ["arn"]),
        (statement_3(), re.compile(r"^.*1$"), ["arn1"]),
        (statement_4(), re.compile(r"^.*2$"), ["arn2"]),
    ],
)
def test_resources_with(statement, pattern, expected_output):
    assert statement.resources_with(pattern) == expected_output


@pytest.mark.parametrize(
    "statement, whitelist, expected_output",
    [
        (statement_principal_1(), ["arn:aws:iam::123456789012:root"], []),
        (
            statement_principal_2(),
            ["arn:aws:iam::AWS-account-ID:user/user-name-1"],
            ["arn:aws:iam::AWS-account-ID:user/UserName2"],
        ),
    ],
)
def test_non_whitelisted_principals(statement, whitelist, expected_output):
    assert statement.non_whitelisted_principals(whitelist) == expected_output