from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session
from datetime import datetime

DATABASE_URL = "sqlite:///./banco1.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# --- MODELOS ---
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    endereco = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=False)

    contas = relationship("Conta", back_populates="cliente")

class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    saldo = Column(Float, default=0.0)
    agencia = Column(String, default="0001")
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="contas")
    transacoes = relationship("Transacao", back_populates="conta")

class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    tipo_de_transacao = Column(String, nullable=False)   # "deposito" ou "saque"
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    conta_id = Column(Integer, ForeignKey("contas.id"))

    conta = relationship("Conta", back_populates="transacoes")

Base.metadata.create_all(bind=engine)
