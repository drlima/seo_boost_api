from typing import Generator

from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    with Session(bind=engine) as db:
        yield db
