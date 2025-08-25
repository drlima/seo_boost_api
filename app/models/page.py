from datetime import datetime

from sqlmodel import Field, SQLModel


class Page(SQLModel, table=True):
    __tablename__ = "pages"

    id: int = Field(primary_key=True, index=True)
    title: str = Field(max_length=255, nullable=False, index=True)
    content: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
