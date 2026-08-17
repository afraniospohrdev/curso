# init_db.py
from db import Base, engine
import models  # garante que LivroDB seja registrado

print("Criando tabelas no banco:", engine.url)
Base.metadata.create_all(bind=engine)
print("Tabelas criadas:", Base.metadata.tables.keys())

