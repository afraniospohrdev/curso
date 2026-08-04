# tests/conftest.py
import pytest
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# sinaliza ambiente de teste para usar sqlite:///:memory:
os.environ.setdefault("PYTEST_RUNNING", "1")

from db import Base, engine
import models  # importa o módulo que define LivroDB

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
