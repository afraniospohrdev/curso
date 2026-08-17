import pytest
from fastapi.testclient import TestClient
from main import app
from db import SessionLocal
from models import LivroDB

client = TestClient(app)

# Fixture que limpa e popula o banco antes dos testes
@pytest.fixture(autouse=True)
def populate_db():
    db = SessionLocal()
    db.query(LivroDB).delete()
    db.commit()
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
