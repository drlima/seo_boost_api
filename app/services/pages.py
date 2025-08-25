from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.page import Page
from app.schemas.page import PageCreate


def create_page(db: Session, data: PageCreate) -> Page:
    page = Page(title=data.title, content=data.content)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


def list_pages(
    db: Session,
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
    order_desc: bool = True,
) -> Iterable[Page]:
    stmt = select(Page)
    if q:
        # filtro simples por título; pode trocar para ilike no Postgres
        stmt = stmt.where(Page.title.contains(q))
    if order_desc:
        stmt = stmt.order_by(Page.created_at.desc())
    else:
        stmt = stmt.order_by(Page.created_at.asc())
    stmt = stmt.offset(offset).limit(min(limit, 200))
    return db.execute(stmt).scalars().all()
