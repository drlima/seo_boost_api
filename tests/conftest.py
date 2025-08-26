import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, delete

from app.core.config import settings
from app.main import app
from app.models.page import Page
from app.models.user import User


@pytest.fixture
def client() -> TestClient:
    client = TestClient(app)
    return client


@pytest.fixture(autouse=True)
def clean_database():
    # Limpar dados antes de cada teste
    engine = create_engine(settings.database_url)
    with Session(engine) as session:
        session.exec(delete(Page))
        session.exec(delete(User))
        session.commit()
    yield



