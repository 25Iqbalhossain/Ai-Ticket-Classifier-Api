from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.db import create_engine, Base
from app.api.routes_ticket import router as ticket_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=create_engine)
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(ticket_router)

@app.get("/")
def root():
    return {"message": "AI Ticket API is running", "docs": "/docs"}
