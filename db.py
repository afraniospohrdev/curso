# db.py (trecho relevante)
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if os.getenv("PYTEST_RUNNING"):
    # respeita DATABASE_URL se definido; caso contrário, usa arquivo local
    DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL)

# se for sqlite com caminho relativo, converte para absoluto
if DATABASE_URL.startswith("sqlite:///"):
    path = DATABASE_URL.replace("sqlite:///", "", 1)
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    DATABASE_URL = f"sqlite:///{path}"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
