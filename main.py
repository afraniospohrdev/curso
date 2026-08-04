# API de livros

# GET, POST, PUT, DELETE

# Get - Buscar os dados dos livros(CREATE)
# Post - Adicionar novos livros(Read)
# Put - Atualizar informações dos livros(Update)
# Delete - Deletar informações dos livros(Delete)

# CRUD

# Create
# Read
# Update
# Delete

# vamos acessar nosso Endpoint
# E vamos acessar os PATH's do nosso Endpoint

# Path ou Rota
# Query Strings

# 200 300 400 500

# Documentação Swagger -> Documentar os endpoints da nossa aplicação (da nossa API)

# Olha, acessa minha documentação swagger nesse endpoint -> http://endpointdelivros/docs/

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os
import redis
import json 
from fastapi import BackgroundTasks
from tasks import fatorial, somar
from celery_app import celery_app
from celery.result import AsyncResult
from kafka_producer import enviar_evento

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import Base

import asyncio

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# Para testes, use banco em memória
if os.getenv("PYTEST_RUNNING"):
    DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

app = FastAPI(
    title="API de Livros",
    description="API para gerenciar catalogo de livros.",
    version="1.0.0",
    contact={ 
        "name":"Afranio Spohr",
        "email":"afraniorogerio@gmail.com"
        }
)

# variveis de ambiente
MEU_USUARIO = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()

livros = []

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

class LivroDB(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, nullable=False)
    autor_livro = Column(String, nullable=False)
    ano_livro = Column(Integer, nullable=False)

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

def salvar_livro_redis(livro_id: int, livro: Livro):
    redis_client.set(f"livro:{livro_id}", json.dumps(livro.dict()))

def deletar_livro_redis(id_livro: int):
    redis_client.delete(f"livro:{id_livro}")

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Essa função tem a responsabilidade de validar o usuario e a senha!
def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuario não autorizado! Credenciais inválidas!!!",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    return credentials
 
@app.get("/")
def hello_world():
    return {"Hello": " World!"}

@app.post("/calcular/soma")
def calcular_soma(a: int, b: int):
    tarefa = somar.delay(a, b)
    redis_client.lpush("tarefas_ids", tarefa.id)
    redis_client.ltrim("tarefas_ids", 0, 49)

    return {
        "task_id": tarefa.id,
        "message":"Tarefa de soma enviada para execução!!"
    }

@app.post("/calcular/fatorial")
def calcular_fatorial(n: int):
    tarefa = fatorial.delay(n)
    redis_client.lpush("tarefas_ids", tarefa.id)
    redis_client.ltrim("tarefas_ids", 0, 49)

    return {
        "task_id": tarefa.id,
        "message":"Tarefa de fatorial enviada para execução!!"
    }

@app.get("/tarefas/recentes")
def listar_tarefas_recentes():
    ids = redis_client.lrange("tarefas_ids", 0, -1)
    tarefas = []

    for task_id in ids:
        resultado = AsyncResult(task_id, app=celery_app)

        tarefas.append({
            "task_id": task_id,
            "status": resultado.status,
            "resultado": resultado.result if resultado.successful() else None
        })

    return {
        "tarefas": tarefas
    }        
     
  
@app.get("/debug/redis")
def ver_livros_redis():
    chaves = redis_client.keys("livro:*")
    livros = []

    for chave in chaves:
        valor = redis_client.get(chave)
        ttl = redis_client.ttl(chave)

        livros.append({"chave": chave, "valor": json.loads(valor), "ttl": ttl})

    return livros

async def chamadas_externas_1():
    await asyncio.sleep(2)
    return "Resposta da chamada externa 1"

async def chamadas_externas_2():
    await asyncio.sleep(2)
    return "Resposta da chamada externa 2"

async def chamadas_externas_3():
    await asyncio.sleep(2)
    return "Resposta da chamada externa 3"

@app.get("/chamadas-externas")
async def chamadas_externas():
    tarefa1 = asyncio.create_task(chamadas_externas_1())
    tarefa2 = asyncio.create_task(chamadas_externas_2())
    tarefa3 = asyncio.create_task(chamadas_externas_3())

    resultado1 = await tarefa1
    resultado2 = await tarefa2
    resultado3 = await tarefa3

    return {
        "mensagem": "Todas as chamadas nas API's foram concluídas com sucesso!",
        "resultado1": resultado1,
        "resultado2": resultado2,
        "resultado3": resultado3
    }

@app.get("/livros")
def get_livros(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estao com os valores invalidos")
    
    cache_key = f"livros:page={page}&limit={limit}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)
    
    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all() 

    if not livros:
        return {
            "page": page,
            "limit": limit,
            "total": 0,
            "livros": []
    }
    
    total_livros = db.query(LivroDB).count()

    resposta = {
        "page": page,
        "limit": limit,
        "total": total_livros,
        "livros": [
            {
                "id": livro.id, 
                "nome_livro": livro.nome_livro, 
                "autor_livro": livro.autor_livro, 
                "ano_livro": livro.ano_livro
            } for livro in livros
        ]
    }

    redis_client.setex(cache_key, 30, json.dumps(resposta))

    return resposta

    # id do livro
    # nome do livro
    # autor do livro
    # ano de lançamento do livro
@app.post("/adiciona")
async def post_livros(livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro, LivroDB.autor_livro == livro.autor_livro, LivroDB.ano_livro == livro.ano_livro).first()
    
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    
    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    salvar_livro_redis(novo_livro.id, livro)

    enviar_evento("livros_eventos", {
        "acao": "criar",
        "livro": livro.dict()
    })
                   
    return {"message": "O livro foi criado com sucesso!"}
    
# Dicionario = HashMap
# Chave -> Valor
   
@app.put("/atualiza/{id_livro}")
async def put_livros(id_livro: int, livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro

    db.commit()
    db.refresh(db_livro)

    salvar_livro_redis(db_livro.id, livro)

    return {"message": "Livro atualizado com sucesso!",}

    
@app.delete("/deletar/{id_livro}")
async def delete_livro(id_livro: int, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    db.delete(db_livro)
    db.commit()

    deletar_livro_redis(id_livro)

    return {"message": "Livro deletado com sucesso!"}

    
# ACID
     
