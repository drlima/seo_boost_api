# routes/pages.py
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.page import PageCreate, PageResponse
from app.services.pages import create_page, list_pages

router = APIRouter(prefix="/pages", tags=["pages"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def create_page_endpoint(payload: PageCreate, db: DbSession) -> PageResponse:
    page = create_page(db, payload)
    return PageResponse.model_validate(page, from_attributes=True)


@router.get("", response_model=list[PageResponse])
def list_pages_endpoint(
    db: DbSession,
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
    order: str = "desc",
) -> list[PageResponse]:
    pages = list_pages(db, q=q, limit=limit, offset=offset, order_desc=(order != "asc"))  # list[Page]
    return [PageResponse.model_validate(p, from_attributes=True) for p in pages]
