from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://searchcraft:searchcraft@localhost:5432/searchcraft"
    MEILISEARCH_URL: str = "http://localhost:7700"
    MEILISEARCH_API_KEY: str = "masterKey"
    OUTBOX_POLL_INTERVAL: int = 2  # seconds
    OUTBOX_BATCH_SIZE: int = 100

    class Config:
        env_file = ".env"

settings = Settings()
