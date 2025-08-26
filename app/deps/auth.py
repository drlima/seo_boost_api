from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session, select

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import User

# Mudança para HTTPBearer - mais apropriado para JWT
security = HTTPBearer()

session_dependency = Annotated[Session, Depends(get_session)]
credentials_dependency = Annotated[HTTPBearer, Depends(security)]


def get_current_user(session: session_dependency, credentials: credentials_dependency) -> User:
    payload = decode_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email = payload["sub"]
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
