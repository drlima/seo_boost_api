from typing import Generator

import pytest
from httpx import ASGITransport, AsyncClient

from app.db import Base, engine
from app.main import app


@pytest.fixture(autouse=True, scope="module")
def _create_db() -> Generator[None, None, None]:
    # Recria as tabelas para a suite (SQLite local)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def async_client() -> Generator[AsyncClient, None, None]:
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    yield client
