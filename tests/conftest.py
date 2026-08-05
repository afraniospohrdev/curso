# tests/conftest.py
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# força modo de teste ANTES de qualquer import que crie engine
os.environ.setdefault("PYTEST_RUNNING", "1")

# limpa módulos que possam ter sido importados antes
for m in ("db", "models", "main"):
    if m in sys.modules:
        del sys.modules[m]

from db import Base, engine
import models  # registra modelos no MetaData

# DEBUG curto (aparecerá nos logs do CI)
print("DEBUG conftest: Base tables before create_all:", list(Base.metadata.tables.keys()))
print("DEBUG conftest: engine id:", id(engine))
print("DEBUG conftest: engine url:", getattr(engine, "url", str(engine)))

# cria as tabelas agora, antes da coleta/import dos testes
Base.metadata.create_all(bind=engine)

import pytest

@pytest.fixture(scope="session", autouse=True)
def teardown_database():
    yield
    Base.metadata.drop_all(bind=engine)
