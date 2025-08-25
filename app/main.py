from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from .db import Base, engine
from .models import page  # noqa: F401
from .routes.pages import router as pages_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="SEO Boost API", lifespan=lifespan)


app.include_router(pages_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "SEO Boost API - OK"}
