from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def create_user_and_token(email: str) -> str:
    client.post("/users", json={"email": email, "password": "123456"})
    r = client.post("/login", json={"email": email, "password": "123456"})
    return r.json()["access_token"]  # type: ignore[no-any-return]


def test_pages_by_owner_only() -> None:
    t1 = create_user_and_token("u1@test.com")
    t2 = create_user_and_token("u2@test.com")

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
