from fastapi.testclient import TestClient


def create_user_and_token(client: TestClient, email: str) -> str:
    client.post("/users", json={"email": email, "password": "123456"})
    r = client.post("/login", json={"email": email, "password": "123456"})
    return r.json()["access_token"]  # type: ignore[no-any-return]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
