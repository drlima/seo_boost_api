from datetime import datetime

from sqlmodel import Field, ForeignKey, SQLModel, String, Text



class SEOData(SQLModel, table=True):
    __tablename__ = "seo_data"

    id: int = Field(primary_key=True)
    page_id: int = Field(ForeignKey("pages.id", ondelete="CASCADE"), unique=True, index=True)
    optimized_title: str | None = Field(String(255))
    optimized_description: str | None = Field(Text)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

