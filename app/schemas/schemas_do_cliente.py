from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from app.schemas.schemas_da_conta import ContaOut

# Schema de entrada para criação de cliente
class ClienteIn(BaseModel):
    nome: str
    cpf: str
    endereco: str
    data_nascimento: str

# Schema de saída para cliente, incluindo suas contas
class ClienteOut(BaseModel):
    id: int
    nome: str
    cpf: str
    endereco: Optional[str] = None   # campo opcional
    data_nascimento: Optional[str] = None  # campo opcional
    contas: List[ContaOut] = Field(default_factory=list)  # lista de contas vinculadas

    model_config = ConfigDict(from_attributes=True)  # permite criar a partir de objetos ORM
