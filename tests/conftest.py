import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("PYTEST_RUNNING", "1")

# limpa módulos que possam ter sido importados antes
for m in ("db", "models", "main"):
    if m in sys.modules:
        del sys.modules[m]

from db import Base, engine
import models  # registra modelos no MetaData

Base.metadata.create_all(bind=engine)

import pytest

@pytest.fixture(scope="session", autouse=True)
def teardown_database():
    yield
    Base.metadata.drop_all(bind=engine)
