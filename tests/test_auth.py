from fastapi.testclient import TestClient
import pytest
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app
from db import SessionLocal
from models import LivroDB

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    mock_redis_client.get.return_value = None

# Fixture que limpa e popula o banco antes dos testes
@pytest.fixture(autouse=True)
def populate_db():
    db = SessionLocal()
    db.query(LivroDB).delete()
    db.commit()
    livro = LivroDB(nome_livro="Teste", autor_livro="Autor", ano_livro=2024)
    db.add(livro)
    db.commit()
    db.close()

def test_autenticacao_usuario_com_sucesso():
    response = client.get("/livros", auth=("admin", "admin"))
    assert response.status_code == 200

def test_autenticacao_usuario_com_erro():
    response = client.get("/livros", auth=("usuario_incorreto", "admin"))
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario não autorizado! Credenciais inválidas!!!"

def test_autenticacao_senha_com_erro():
    response = client.get("/livros", auth=("admin", "senha_incorreta"))
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario não autorizado! Credenciais inválidas!!!"

def test_autenticacao_email_vazio():
    response = client.get("/livros", auth=("", "admin"))
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario não autorizado! Credenciais inválidas!!!"

def test_autenticacao_senha_vazia():
    response = client.get("/livros", auth=("admin", ""))
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario não autorizado! Credenciais inválidas!!!"

def test_autenticacao_senha_curta():
    response = client.get("/livros", auth=("admin", "12"))
    assert response.status_code == 401
