from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Configuration for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

# Create a SQLAlchemy engine to manage database connections
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SQLAlchemy session factory to create new sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
