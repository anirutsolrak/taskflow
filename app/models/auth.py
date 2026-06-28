from pydantic import BaseModel

class CriarUsuario(BaseModel):
    email: str
    senha: str

class LoginUsuario(BaseModel):
    email: str
    senha: str