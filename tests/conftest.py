import pytest
import sys
import os

# adiciona raiz do projeto ao sys.path para importar main.py e módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# sinaliza ambiente de teste (opcional, se seu main.py respeitar essa variável)
os.environ.setdefault("PYTEST_RUNNING", "1")

# importa engine e Base do seu main (ou do módulo onde estão definidos)
from main import engine, Base

# IMPORTE AQUI os módulos que definem os modelos (substitua pelo nome real)
# Exemplo: se o modelo Livro está em models.py ou em app/models.py
try:
    # se seus modelos estão em models.py na raiz
    import models  # noqa: F401
except Exception:
    # se estiverem em app/models.py
    try:
        from app import models  # noqa: F401
    except Exception:
        # fallback: tente importar diretamente a classe
        try:
            from models import Livro  # noqa: F401
        except Exception:
            pass

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Garante que todos os modelos foram importados e cria as tabelas antes dos testes.
    """
    # Cria todas as tabelas conhecidas por Base
    Base.metadata.create_all(bind=engine)
    yield
    # Opcional: limpa após os testes
    Base.metadata.drop_all(bind=engine)
