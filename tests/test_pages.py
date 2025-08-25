import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_root_ok(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"].startswith("SEO Boost API")


@pytest.mark.asyncio
async def test_create_and_list_pages(client: TestClient) -> None:
    # cria
    payload = {"title": "Home", "content": "Bem-vindo"}
    r = client.post("/pages", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["id"] > 0
    assert created["title"] == "Home"

    # lista
    r2 = client.get("/pages")
    assert r2.status_code == 200
    items = r2.json()
    assert isinstance(items, list)
    assert any(p["title"] == "Home" for p in items)


@pytest.mark.asyncio
async def test_validation_error_title_required(client: TestClient) -> None:
    response = client.post("/pages", json={"title": "", "content": "x"})
    assert response.status_code == 422
