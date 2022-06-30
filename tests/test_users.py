import pytest
# from api.models import db, User


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b"No username provided for user."),
        ('sasha', '', b"No password provided for user."),
        ('sasha27&(*(', 'test', b"Invalid character in username."),
))
def test_user_validate_input(client, username, password, message):
    response = client.post(
        '/user',
        json={'username': username, 'password': password}
    )
    assert response.status_code == 422, "Bad response code"
    assert message in response.data, f"Bad response message, it should be {message}"
