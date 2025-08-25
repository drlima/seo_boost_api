from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Page(SQLModel, table=True):
    __tablename__ = "pages"

    id: int = Field(primary_key=True, index=True)
    title: str = Field(max_length=255, nullable=False, index=True)
    content: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    owner_id: int = Field(foreign_key="users.id", nullable=True)
    owner: "User" = Relationship(back_populates="pages")
