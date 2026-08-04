import pytest
import sys, os

# adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


