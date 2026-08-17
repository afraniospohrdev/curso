# tests/conftest.py
import os, sys
import pytest
from db import SessionLocal

@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Defina PYTEST_RUNNING antes de importar db/models
os.environ.setdefault("PYTEST_RUNNING", "1")

# Remova módulos que possam ter sido importados antes
for m in ("db", "models", "main"):
    if m in sys.modules:
        del sys.modules[m]

from db import Base, engine
import models  # registra modelos no MetaData

print("DEBUG conftest: Base tables before create_all:", list(Base.metadata.tables.keys()))
print("DEBUG conftest: engine id:", id(engine))
print("DEBUG conftest: engine url:", getattr(engine, "url", str(engine)))

Base.metadata.create_all(bind=engine)

import pytest

@pytest.fixture(scope="session", autouse=True)
def teardown_database():
    yield
    Base.metadata.drop_all(bind=engine)
