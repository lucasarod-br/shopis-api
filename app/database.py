from typing import Annotated
from fastapi import Depends

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    from app.models import user, address, role, activation_token, category, product, brand
    Base.metadata.create_all(bind=engine)

def check_database_health(db: Session):
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise e