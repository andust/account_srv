from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


from src.config.envirenment import get_settings

Base = declarative_base()

_S = get_settings()
DATABASE_URL = f"postgresql://{_S.DB_USER}:{_S.DB_PASSWORD}@{_S.DB_HOST}:{_S.DB_PORT}/{_S.DB_NAME}"

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        print(db)
        db.close()
