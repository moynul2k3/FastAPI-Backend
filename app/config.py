from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True
    ENV: str = "development"
    
    # DATABASE_URL: str = "mysql://root:root@localhost:3306/mydb"
    # DATABASE_URL: str = "postgres://postgres:root@localhost:5432/mydb"
    DATABASE_URL: str = "postgres://neondb_owner:npg_kY0Qo2RUXZVL@ep-damp-scene-adfwy4vs-pooler.c-2.us-east-1.aws.neon.tech/neondb"
    SECRET_KEY: Optional[str] = "c6dcf58058a6ce5204199818a25eed7eb58b6758a20df0385e29dbea6b49873dccad7449f8022dc193da4616ba10c97457aa2e16e0b2c5b0e5555fe1ac492aa1"

    class Config:
        env_file = ".env"

settings = Settings()
TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL or "sqlite://db.sqlite3"   # fallback
    },
    "apps": {
        "models": {
            "models": ["applications.user.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "UTC",
}

