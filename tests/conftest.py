# tests/conftest.py
import os
import sys

# garante que a raiz do projeto esteja no PYTHONPATH
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# sinaliza ambiente de teste ANTES de qualquer import que crie engine
os.environ.setdefault("PYTEST_RUNNING", "1")

# agora importe db e modelos e crie as tabelas imediatamente
from db import Base, engine
# importe o módulo que define LivroDB (ajuste se estiver em outro caminho)
import models  # noqa: F401

# debug opcional: listar tabelas conhecidas
print("DEBUG: tabelas registradas no MetaData:", list(Base.metadata.tables.keys()))

# cria as tabelas agora, antes da coleta/import dos testes
Base.metadata.create_all(bind=engine)

import pytest

@pytest.fixture(scope="session", autouse=True)
def teardown_database():
    # fixture apenas para garantir limpeza ao final da sessão
    yield
    Base.metadata.drop_all(bind=engine)
