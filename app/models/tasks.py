from pydantic import BaseModel 

class CriarTarefa(BaseModel):
    titulo: str
    concluida: bool = False

class AtualizarTarefa(BaseModel):
    titulo: str | None = None
    concluida: bool | None = None