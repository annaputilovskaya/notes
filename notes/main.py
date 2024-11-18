from contextlib import asynccontextmanager

import uvicorn
from core.config import settings
from core.database import db_helper
from fastapi import FastAPI
from notices.routers import router as notes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(title="Notes", lifespan=lifespan)

main_app.include_router(notes_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
