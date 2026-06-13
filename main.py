from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import init_db
from routes.tickets import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initializes your clean SQLite tables on system container spin-up
    await init_db()
    yield

app = FastAPI(title="Datastraw CRM", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)