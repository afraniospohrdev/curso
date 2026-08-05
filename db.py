# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if os.getenv("PYTEST_RUNNING"):
    DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# debug opcional
print("DEBUG db: engine id:", id(engine))
print("DEBUG db: engine url:", getattr(engine, "url", str(engine)))
print("DEBUG db: Base tables at import:", list(Base.metadata.tables.keys()))
