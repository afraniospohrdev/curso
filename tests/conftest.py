import pytest
import sys, os

# adiciona raiz ao sys.path para importar main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Cria todas as tabelas antes dos testes
    Base.metadata.create_all(bind=engine)
    yield
    # Limpa depois (opcional)
    Base.metadata.drop_all(bind=engine)




