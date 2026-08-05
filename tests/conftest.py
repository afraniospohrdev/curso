# tests/conftest.py
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# força o modo de teste ANTES de importar db/main/models
os.environ.setdefault("PYTEST_RUNNING", "1")

# opcional: se você preferir usar arquivo sqlite persistente durante CI,
# descomente a linha abaixo (útil para diagnosticar problemas de in-memory)
# os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from db import Base, engine
# importe o módulo que define LivroDB (ajuste se estiver em app.models)
import models  # noqa: F401

# debug curto para confirmar que o modelo foi registrado
print("DEBUG: tabelas registradas no MetaData:", list(Base.metadata.tables.keys()))
print("DEBUG: engine url:", getattr(engine, "url", str(engine)))
print("DEBUG: engine id:", id(engine))

# cria as tabelas agora, antes da coleta/import dos testes
Base.metadata.create_all(bind=engine)

import pytest

@pytest.fixture(scope="session", autouse=True)
def teardown_database():
    yield
    Base.metadata.drop_all(bind=engine)
