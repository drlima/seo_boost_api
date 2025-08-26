import pytest
from fastapi.testclient import TestClient


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def create_user_and_token(client: TestClient, email: str) -> str:
    client.post("/users", json={"email": email, "password": "123456"})
    r = client.post("/login", json={"email": email, "password": "123456"})
    return r.json()["access_token"]  # type: ignore[no-any-return]


@pytest.mark.asyncio
async def test_root_ok(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"].startswith("SEO Boost API")


@pytest.mark.asyncio
async def test_create_and_list_pages(client: TestClient) -> None:
    # Create user and get token
    token = create_user_and_token(client, "test@example.com")

    # Create page
    payload = {"title": "Home", "content": "Bem-vindo"}
    r = client.post("/pages", json=payload, headers=auth_header(token))
    assert r.status_code == 201
    created = r.json()
    assert created["id"] > 0
    assert created["title"] == "Home"

    # List pages
    r2 = client.get("/pages", headers=auth_header(token))
    assert r2.status_code == 200
    items = r2.json()
    assert isinstance(items, list)
    assert any(p["title"] == "Home" for p in items)


@pytest.mark.asyncio
async def test_validation_error_title_required(client: TestClient) -> None:
    # Create user and get token
    token = create_user_and_token(client, "test2@example.com")

    response = client.post("/pages", json={"title": "", "content": "x"}, headers=auth_header(token))
    assert response.status_code == 422
