from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas_auth import RegisterUsuario, UsuarioOut, LoginUsuario, TokenOut
from app.service.service_registro_login import ServiceAuth
from app.autenticacao_bancaria.auth import verificar_token
from app.database.session import get_session, AsyncSession

router = APIRouter()

@router.post(
        "/register",
        response_model=UsuarioOut
)
async def register(
    data: RegisterUsuario, 
    session: AsyncSession = Depends(get_session)
):
    usuario = await ServiceAuth.registrar_usuario(data,session)
    if usuario == 'usuario_ja_existe':
        raise HTTPException(status_code=400,detail='Usuario ja existe')
    
    return usuario


@router.post(
        "/login",
        response_model=TokenOut
)
async def login(
    data: LoginUsuario, 
    session: AsyncSession = Depends(get_session)
):
    usuario = await ServiceAuth.logar_usuario(data,session)
    if usuario == 'credenciais_invalidas':
        raise HTTPException(status_code=400,detail='Credenciais invalidas')
    
    return usuario

'''
@router.get(
        "/protected"
)
async def protected_route(username: str = Depends(verificar_token)):
    return {"msg": f"Bem-vindo {username}, você acessou uma rota protegida!"}
'''