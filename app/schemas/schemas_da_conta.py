from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from app.schemas.schemas_da_transacao import TransacaoOut

# Schema de entrada para criação de conta
class ContaIn(BaseModel):
    numero: int
    cpf: str

# Schema de saída para conta, incluindo histórico de transações
class ContaOut(BaseModel):
    numero: int
    agencia: str
    saldo: float
    titular: Optional[str] = None  # nome do cliente associado
    historico: List[TransacaoOut] = Field(default_factory=list)  # lista de transações

    model_config = ConfigDict(from_attributes=True)  # permite criar a partir de objetos ORM

# Schema de saída para confirmação de exclusão de conta
class DeletarConta(BaseModel):
    mensagem: str
