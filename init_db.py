# init_db.py
from db import Base, engine
import models

print("Criando tabelas no banco:", engine.url)
Base.metadata.create_all(bind=engine)
