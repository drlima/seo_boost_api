from typing import Iterable

from sqlmodel import Session, select

from app.models.page import Page
from app.schemas.page import PageCreate


async def create_page(db: Session, data: PageCreate) -> Page:
    page = Page(title=data.title, content=data.content)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


async def list_pages(
    db: Session,
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
    order_desc: bool = True,
) -> Iterable[Page]:
    stmt = select(Page)
    if q:
        # filtro simples por título; pode trocar para ilike no Postgres
        stmt = stmt.where(Page.title.contains(q))  # type: ignore[attr-defined]
    else:
        stmt = stmt.order_by(Page.created_at.asc())    # type: ignore[attr-defined]
    stmt = stmt.offset(offset).limit(min(limit, 200))
    result = db.exec(stmt)
    return result.all()
