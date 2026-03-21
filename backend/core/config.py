from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    APP_NAME: str = "AI Summarization API"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: SecretStr
    algorithm: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL_PATH: str = "models/vit5"
    VECTOR_DB_PATH: str = "data/vector_store"

    @property
    def sqlalchemy_database_url(self) -> str:
        return self.DATABASE_URL


settings = Settings()