# tests/conftest.py
import pytest
from db import Base, engine, SessionLocal
import models  # garante que LivroDB seja registrado

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # cria todas as tabelas antes de qualquer teste
    Base.metadata.create_all(bind=engine)
    yield
    # opcional: limpar depois
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
