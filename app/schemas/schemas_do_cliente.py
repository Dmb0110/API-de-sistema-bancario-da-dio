from pydantic import BaseModel, ConfigDict

class ClienteIn(BaseModel):
    nome: str
    cpf: str
    endereco: str
    data_nascimento: str

class ClienteOut(BaseModel):
    id: int
    nome: str
    cpf: str
    endereco: str
    data_nascimento: str

    model_config = ConfigDict(
        from_attributes=True
    )
