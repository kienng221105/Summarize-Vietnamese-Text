from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings
DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


