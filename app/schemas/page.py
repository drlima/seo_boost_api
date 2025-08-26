from datetime import datetime

from pydantic import BaseModel, Field


class PageBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str | None = None


class PageCreate(PageBase):
    pass


class PageUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PageResponse(PageBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
