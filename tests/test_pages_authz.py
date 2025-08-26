from typing import Callable

from fastapi.testclient import TestClient

from tests.utils import create_user_and_token, auth_header


def test_pages_by_owner_only(client: TestClient) -> None:
    t1 = create_user_and_token(client, "u1@test.com")
    t2 = create_user_and_token(client, "u2@test.com")

    # user1 cria
    r = client.post("/pages", json={"title": "t", "content": "c"}, headers=auth_header(t1))
    assert r.status_code == 201
    page_id = r.json()["id"]

    # user2 não vê na listagem
    r = client.get("/pages", headers=auth_header(t2))
    assert r.status_code == 200
    assert all(p["id"] != page_id for p in r.json())

    # user2 não acessa diretamente
    r = client.get(f"/pages/{page_id}", headers=auth_header(t2))
    assert r.status_code in (403, 404)  # escolhemos 404 no código

    # user1 atualiza e deleta
    r = client.put(f"/pages/{page_id}", json={"title": "t2"}, headers=auth_header(t1))
    assert r.status_code == 200 and r.json()["title"] == "t2"
    r = client.delete(f"/pages/{page_id}", headers=auth_header(t1))
    assert r.status_code == 204
