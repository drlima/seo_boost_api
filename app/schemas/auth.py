from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105


class LoginInput(BaseModel):
    email: EmailStr
    password: str
