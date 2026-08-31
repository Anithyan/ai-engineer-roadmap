# tests/test_debug_login.py
def test_login_debug(client, seed_test_user):
    resp = client.post(
        "/auth/token", data={"username": "demo@test.com", "password": "secret123"}
    )
    print("STATUS:", resp.status_code)
    print("BODY:", resp.json())
