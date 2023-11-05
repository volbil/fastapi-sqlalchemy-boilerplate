from client_requests import request_permission_example
from fastapi import status


async def test_permission_example(
    client,
    create_test_user_admin,
    get_test_token,
):
    # Make request to protected endpoint
    response = await request_permission_example(client, get_test_token)

    # And get current user
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "username"


async def test_permission_example_bad(
    client,
    create_test_user,
    get_test_token,
):
    # Make request to protected endpoint
    response = await request_permission_example(client, get_test_token)

    # And fail miserably
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["code"] == "permission:denied"
