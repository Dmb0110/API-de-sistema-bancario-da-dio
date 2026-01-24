from sqlalchemy import Column, Integer, String
from app.database.session import Base

# Modelo User representa a tabela "users" no banco de dados
class User(Base):
    __tablename__ = "users"

    # Chave primária única para cada usuário
    id = Column(Integer, primary_key=True, index=True)

    # Nome de usuário único, obrigatório e indexado para buscas rápidas
    username = Column(String(50), unique=True, index=True, nullable=False)

    # Senha armazenada em formato hash (nunca em texto puro)
    hashed_password = Column(String(255), nullable=False)
