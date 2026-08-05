# models.py
from sqlalchemy import Column, Integer, String
from db import Base

class LivroDB(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, nullable=False)
    autor_livro = Column(String, nullable=False)
    ano_livro = Column(Integer, nullable=False)

# debug opcional
print("DEBUG models: Base tables at import:", list(Base.metadata.tables.keys()))
