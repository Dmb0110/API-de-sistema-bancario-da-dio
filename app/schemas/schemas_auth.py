from pydantic import BaseModel

class RegisterUsuario(BaseModel):
    username: str
    password: str

class LoginUsuario(BaseModel):
    username: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
