from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.models.auth import CriarUsuario, LoginUsuario

router = APIRouter()

# Rota para criar um novo usuário
@router.post("/registro")
def criar_usuario(usuario: CriarUsuario):
    response = supabase.auth.sign_up({"email": usuario.email, "password": usuario.senha})
    if response.user is None:
        raise HTTPException(status_code=400, detail="Erro ao criar usuário")
    return {"mensagem": "Usuário criado com sucesso", "user_id": response.user.id}

# Rota para login de usuário
@router.post("/login")
def login_usuario(usuario: LoginUsuario):
    response = supabase.auth.sign_in_with_password({"email": usuario.email, "password": usuario.senha})
    if response.user is None or response.session is None:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"mensagem": "Login bem-sucedido", "user_id": response.user.id, "access_token": response.session.access_token, "token_type": "bearer"}
    