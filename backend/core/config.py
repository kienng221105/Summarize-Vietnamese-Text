from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Summarization API"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL_PATH: str = "models/vit5"
    VECTOR_DB_PATH: str = "data/vector_store"

    class Config:
        env_file = ".env"


settings = Settings()