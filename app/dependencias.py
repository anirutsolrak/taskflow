from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from app.db.supabase import supabase

seguranca = HTTPBearer()

def obter_usuario_atual(credenciais: HTTPAuthorizationCredentials = Depends(seguranca)):
    token = credenciais.credentials
    response = supabase.auth.get_user(token)
    usuario = response.user #type: ignore
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario