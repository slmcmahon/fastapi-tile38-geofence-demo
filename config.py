from pydantic import BaseModel
import os


class Settings(BaseModel):
    APP_NAME: str = os.environ.get("APP_NAME", "gpsdemo")
    APP_VERSION: str = os.environ.get("APP_VERSION", "0.1.0")
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = os.environ.get("PORT", 8000)
    MONGO_CONNECTION_STRING: str = os.environ.get(
        "MONGO_CONNECTION_STRING", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.environ.get("MONGO_DB_NAME", "gpsdemo")
    TILE38_CONNECTION_STRING: str = os.environ.get(
        "TILE38_CONNECTION_STRING", "localhost:9851")


settings = Settings()
