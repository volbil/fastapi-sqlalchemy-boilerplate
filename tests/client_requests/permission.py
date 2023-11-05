def request_permission_example(client, token):
    return client.get("/permission/example", headers={"Auth": token})
