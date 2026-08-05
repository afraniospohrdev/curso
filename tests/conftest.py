# tests/conftest.py
import os
import sys
import importlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 1) força modo de teste ANTES de qualquer import que crie engine
os.environ.setdefault("PYTEST_RUNNING", "1")

# 2) remove módulos que possam ter sido importados antes (garante re-criação correta do engine)
for m in ("db", "models", "main"):
    if m in sys.modules:
        del sys.modules[m]

# 3) agora importe db e modelos com o PYTEST_RUNNING já definido
from db import Base, engine
import models  # garante que LivroDB seja registrado no MetaData

# debug curto (remova depois)
print("DEBUG conftest: Base tables before create_all:", list(Base.metadata.tables.keys()))
print("DEBUG conftest: engine id:", id(engine))
print("DEBUG conftest: engine url:", getattr(engine, "url", str(engine)))

# 4) cria as tabelas agora, antes da coleta/import dos testes
Base.metadata.create_all(bind=engine)

import pytest

@pytest.fixture(scope="session", autouse=True)
def teardown_database():
    yield
    Base.metadata.drop_all(bind=engine)
