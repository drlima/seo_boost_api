from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, String

if TYPE_CHECKING:
    from .page import Page


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, index=True)
    email: str = Field(String(255), unique=True, index=True)
    hashed_password: str = Field(String(255))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    pages: list["Page"] = Relationship(back_populates="owner", cascade_delete=True)
