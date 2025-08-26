from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginInput, Token
from app.schemas.user import UserCreate, UserOut

auth_router = APIRouter(tags=["auth"])
session_dependency = Annotated[Session, Depends(get_session)]


@auth_router.post("/users", response_model=UserOut, status_code=201)
def signup(data: UserCreate, session: session_dependency) -> UserOut:
    exists = session.exec(select(User).where(User.email == data.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserOut(id=user.id, email=user.email)


@auth_router.post("/login", response_model=Token)
def login(data: LoginInput, session: session_dependency) -> Token:
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return Token(access_token=token)
