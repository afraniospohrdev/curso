import pytest
from main import Base, engine, SessionLocal

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Limpa depois (opcional)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Fornece uma sessão de banco para os testes"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


