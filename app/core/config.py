
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Para dev/local: sqlite. Em produção, definir POSTGRES_URL no ambiente.
    DATABASE_URL: str = "sqlite:///./seo_boost_dev.db"

    # Configurações extras
    model_config = SettingsConfigDict(
        env_file=".env",           # Arquivo .env opcional
        env_file_encoding="utf-8",  # Codificação
        extra="ignore"             # Ignorar variáveis extras
    )


settings = Settings()
