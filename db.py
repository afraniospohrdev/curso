# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# se estivermos rodando testes, force in-memory (opcional) — mas CI usará arquivo se você setar DATABASE_URL no workflow
if os.getenv("PYTEST_RUNNING"):
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# connect_args só para sqlite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DEBUG opcional (remova depois)
print("DEBUG db: engine id:", id(engine))
print("DEBUG db: engine url:", getattr(engine, "url", str(engine)))
print("DEBUG db: Base tables at import:", list(Base.metadata.tables.keys()))
