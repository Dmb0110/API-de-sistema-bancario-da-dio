from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

class TransacaoIn(BaseModel):
    numero_conta: int
    tipo_de_transacao: str
    valor: float

class TransacaoOut(BaseModel):
    tipo_de_transacao: str
    valor: float
    data: str

    model_config = ConfigDict(
        from_attributes=True
    )

    @field_validator("data", mode="before") 
    def formatar_data(cls, v): 
        if isinstance(v, datetime): 
            return v.strftime("%d-%m-%Y %H:%M:%S") 
        return v

class MensagemOut(BaseModel):
    mensagem: str
