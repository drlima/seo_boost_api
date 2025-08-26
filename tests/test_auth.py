from fastapi.testclient import TestClient


def test_signup_and_login(client: TestClient) -> None:
    # signup
    r = client.post("/users", json={"email": "a@a.com", "password": "123456"})
    assert r.status_code == 201
    # login
    r = client.post("/login", json={"email": "a@a.com", "password": "123456"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token
