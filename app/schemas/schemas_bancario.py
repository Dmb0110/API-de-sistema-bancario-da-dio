from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from app.models.models_bancario import SessionLocal
from typing import List

app = FastAPI()

# --- Dependência de sessão ---
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schemas Pydantic ---
class ClienteIn(BaseModel):
    nome: str
    cpf: str
    endereco: str
    data_nascimento: str

class ContaIn(BaseModel):
    numero: int
    cpf_cliente: str

class TransacaoIn(BaseModel):
    numero_conta: int
    tipo_de_transacao: str
    valor: float

class TransacaoOut(BaseModel):
    tipo_de_transacao: str
    valor: float
    data: str

class ContaOut(BaseModel):
    numero: int
    agencia: str
    saldo: float
    titular: str
    historico: List[TransacaoOut]
