import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_ok(async_client: AsyncClient) -> None:
    r = await async_client.get("/")
    assert r.status_code == 200
    assert r.json()["message"].startswith("SEO Boost API")


@pytest.mark.asyncio
async def test_create_and_list_pages(async_client: AsyncClient) -> None:
    # cria
    payload = {"title": "Home", "content": "Bem-vindo"}
    r = await async_client.post("/pages", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["id"] > 0
    assert created["title"] == "Home"

    # lista
    r2 = await async_client.get("/pages")
    assert r2.status_code == 200
    items = r2.json()
    assert isinstance(items, list)
    assert any(p["title"] == "Home" for p in items)


@pytest.mark.asyncio
async def test_validation_error_title_required(async_client: AsyncClient) -> None:
    response = await async_client.post("/pages", json={"title": "", "content": "x"})
    assert response.status_code == 422
