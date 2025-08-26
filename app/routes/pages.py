from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.deps.auth import get_current_user
from app.models.page import Page
from app.models.user import User
from app.schemas.page import PageCreate, PageResponse, PageUpdate

pages_router = APIRouter(prefix="/pages", tags=["pages"])
session_dependency = Annotated[Session, Depends(get_session)]
user_dependency = Annotated[User, Depends(get_current_user)]


@pages_router.post("", response_model=PageResponse, status_code=201)
def create_page(data: PageCreate, session: session_dependency, user: user_dependency) -> PageResponse:
    page = Page(title=data.title, content=data.content, owner_id=user.id)
    session.add(page)
    session.commit()
    session.refresh(page)
    return PageResponse(id=page.id, title=page.title, content=page.content, created_at=page.created_at)


@pages_router.get("", response_model=list[PageResponse])
def list_pages(session: session_dependency, user: user_dependency) -> list[PageResponse]:
    pages = session.exec(select(Page).where(Page.owner_id == user.id)).all()
    return [PageResponse(id=p.id, title=p.title, content=p.content, created_at=p.created_at) for p in pages]


@pages_router.get("/{page_id}", response_model=PageResponse)
def get_page(page_id: int, session: session_dependency, user: user_dependency) -> PageResponse:
    page = session.get(Page, page_id)
    if not page or page.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Page not found")
    return PageResponse(id=page.id, title=page.title, content=page.content, created_at=page.created_at)


@pages_router.put("/{page_id}", response_model=PageResponse)
def update_page(page_id: int, data: PageUpdate, session: session_dependency, user: user_dependency) -> PageResponse:
    page = session.get(Page, page_id)
    if not page or page.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Page not found")
    if data.title is not None:
        page.title = data.title
    if data.content is not None:
        page.content = data.content
    session.add(page)
    session.commit()
    session.refresh(page)
    return PageResponse(id=page.id, title=page.title, content=page.content, created_at=page.created_at)


@pages_router.delete("/{page_id}", status_code=204)
def delete_page(page_id: int, session: session_dependency, user: user_dependency) -> None:
    page = session.get(Page, page_id)
    if not page or page.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Page not found")
    session.delete(page)
    session.commit()
