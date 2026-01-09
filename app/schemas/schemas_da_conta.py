from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.schemas_da_transacao import TransacaoOut

class ContaIn(BaseModel):
    numero: int
    cpf: str

class ContaOut(BaseModel):
    numero: int
    agencia: str
    saldo: float
    titular: Optional[str] = None
    historico: Optional[List[TransacaoOut]] =[]

    model_config = ConfigDict(
        from_attributes=True
    )

class DeletarConta(BaseModel):
    mensagem: str
    