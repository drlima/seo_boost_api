from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlmodel import SQLModel

from .db import engine
from .models import page  # noqa: F401
from .routes.pages import pages_router as pages_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="SEO Boost API", lifespan=lifespan)


app.include_router(pages_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "SEO Boost API - OK"}
