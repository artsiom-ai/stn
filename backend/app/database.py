from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

connect_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite thread safety - for SQLAlchemy 2.x use different approach
    pass  # SQLAlchemy 2.x handles this differently

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()