import pytest
from main import Base, engine   # importa direto da raiz

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Cria todas as tabelas antes dos testes
    Base.metadata.create_all(bind=engine)
    yield
    # Opcional: limpar depois
    Base.metadata.drop_all(bind=engine)

