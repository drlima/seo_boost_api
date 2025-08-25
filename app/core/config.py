import os

from pydantic import BaseModel


class Settings(BaseModel):
    # Para dev/local: sqlite. Em produção, definir POSTGRES_URL no ambiente.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./seo_boost_dev.db")


settings = Settings()
