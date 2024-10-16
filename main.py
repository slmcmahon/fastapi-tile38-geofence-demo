from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

from routers.features import router as features_router
from routers.geofences import router as geofences_router
from config import settings
from pyle38 import Tile38


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    app.mongodb = app.mongodb_client[settings.MONGO_DB_NAME]
    app.t38 = Tile38(url=settings.TILE38_CONNECTION_STRING)
    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(features_router)
app.include_router(geofences_router)


@app.get("/")
async def read_root():
    return f"{settings.APP_NAME} {settings.APP_VERSION}"
