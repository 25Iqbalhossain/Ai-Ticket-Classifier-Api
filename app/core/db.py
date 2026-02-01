from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


class Base(DeclarativeBase):
    pass

# window's database url format fix
create_engine = create_engine(settings.DATABASE_URL, echo=True)

# start session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()