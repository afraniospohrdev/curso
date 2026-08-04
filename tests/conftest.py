import pytest
import sys
import os

# adiciona raiz do projeto ao sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# sinaliza ambiente de teste (opcional, se main.py respeitar)
os.environ.setdefault("PYTEST_RUNNING", "1")

# importa Base e engine do seu main (ajuste se estiver em outro módulo)
from main import Base, engine

# tenta importar o módulo que define LivroDB em vários caminhos comuns
_imported_model = False
_import_errors = []

try:
    import models  # raiz/models.py
    _imported_model = True
except Exception as e:
    _import_errors.append(("models", str(e)))
    try:
        from app import models as app_models  # app/models.py
        _imported_model = True
    except Exception as e2:
        _import_errors.append(("app.models", str(e2)))
        try:
            from src import models as src_models  # src/models.py
            _imported_model = True
        except Exception as e3:
            _import_errors.append(("src.models", str(e3)))
            # tentativa direta por nome de classe (se models.py não for pacote)
            try:
                from models import LivroDB  # noqa: F401
                _imported_model = True
            except Exception as e4:
                _import_errors.append(("from models import LivroDB", str(e4)))

# opcional: debug prints para CI local (remova se preferir silêncio)
if not _imported_model:
    print("WARNING: não foi possível importar o módulo de modelos automaticamente.")
    for name, err in _import_errors:
        print(f"  tentativa {name} falhou: {err}")

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Garante que todos os modelos foram importados e cria as tabelas antes dos testes.
    """
    # Cria todas as tabelas conhecidas por Base (inclui 'livros' se o modelo foi importado)
    Base.metadata.create_all(bind=engine)
    yield
    # Opcional: limpa após os testes
    Base.metadata.drop_all(bind=engine)
