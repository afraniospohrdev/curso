# tests/conftest.py
import pytest
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# sinaliza ambiente de teste para main.py usar sqlite:///:memory:
os.environ.setdefault("PYTEST_RUNNING", "1")

from main import Base, engine

# importe explicitamente o módulo que contém LivroDB
# ajuste o import abaixo se o arquivo estiver em outro caminho
import models  # se o arquivo for models.py na raiz
# se estiver em app/models.py, use: from app import models

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
