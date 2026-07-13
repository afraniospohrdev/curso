from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, LivroDB, app, sessao_db

DATABASE_URL_TEST = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

# sobrescreve a dependência para usar o banco de teste
def override_sessao_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[sessao_db] = override_sessao_db

client = TestClient(app)

# Fixture que popula o banco
import pytest

@pytest.fixture(autouse=True)
def popular_db():
    db = TestingSessionLocal()
    livros = [
        LivroDB(nome_livro="A Revolução dos Bichos", autor_livro="George Orwell", ano_livro=1945),
        LivroDB(nome_livro="1984", autor_livro="George Orwell", ano_livro=1949),
        LivroDB(nome_livro="Dom Casmurro", autor_livro="Machado de Assis", ano_livro=1899),
        LivroDB(nome_livro="Memórias Póstumas de Brás Cubas", autor_livro="Machado de Assis", ano_livro=1881),
        LivroDB(nome_livro="O Primo Basílio", autor_livro="Eça de Queirós", ano_livro=1878),
        LivroDB(nome_livro="O Alienista", autor_livro="Machado de Assis", ano_livro=1882),
        LivroDB(nome_livro="Grande Sertão: Veredas", autor_livro="Guimarães Rosa", ano_livro=1956),
        LivroDB(nome_livro="Capitães da Areia", autor_livro="Jorge Amado", ano_livro=1937),
        LivroDB(nome_livro="O Cortiço", autor_livro="Aluísio Azevedo", ano_livro=1890),
        LivroDB(nome_livro="Iracema", autor_livro="José de Alencar", ano_livro=1865),
    ]
    db.add_all(livros)
    db.commit()
    db.close()

def test_get_books():
    response = client.get("/livros", auth=("admin", "admin"))
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["livros"]) == 10
    assert data["livros"][0]["nome_livro"] == "A Revolução dos Bichos"
