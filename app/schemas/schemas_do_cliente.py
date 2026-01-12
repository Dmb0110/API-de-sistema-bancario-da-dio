from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from app.schemas.schemas_da_conta import ContaOut

class ClienteIn(BaseModel):
    nome: str
    cpf: str
    endereco: str
    data_nascimento: str

class ClienteOut(BaseModel):
    id: int
    nome: str
    cpf: str
    endereco: Optional[str] = None
    data_nascimento: Optional[str] = None
    contas: List[ContaOut] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True
    )
