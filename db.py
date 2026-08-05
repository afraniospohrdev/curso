# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Sempre leia DATABASE_URL do ambiente; não force :memory: automaticamente
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Se for sqlite com caminho relativo, converte para absoluto
if DATABASE_URL.startswith("sqlite:///"):
    path = DATABASE_URL.replace("sqlite:///", "", 1)
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    DATABASE_URL = f"sqlite:///{path}"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DEBUG opcional (remova depois)
print("DEBUG db: engine id:", id(engine))
print("DEBUG db: engine url:", getattr(engine, "url", str(engine)))
print("DEBUG db: Base tables at import:", list(Base.metadata.tables.keys()))
