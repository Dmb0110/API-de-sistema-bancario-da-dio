from pydantic import BaseModel

# Schema para registrar novo usuário (entrada)
class RegisterUsuario(BaseModel):
    username: str
    password: str

# Schema para login de usuário (entrada)
class LoginUsuario(BaseModel):
    username: str
    password: str

# Schema de saída ao retornar dados do usuário
class UsuarioOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # permite criar a partir de objetos ORM

# Schema de saída para o token JWT
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"  # padrão de autenticação Bearer
