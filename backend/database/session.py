from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/mydatabase"
engine = create_engine(settings.sqlalchemy_database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  