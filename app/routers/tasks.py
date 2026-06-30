from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase import supabase
from app.models.tasks import CriarTarefa, AtualizarTarefa
from app.dependencias import obter_usuario_atual

router = APIRouter()

#listar todas as tarefas
@router.get("/")
def listar_tarefas(usuario_atual = Depends(obter_usuario_atual)):
    response = supabase.table("tarefas").select("*").execute()
    return response.data

#criar tarefa
@router.post("/")
def criar_tarefa(tarefa: CriarTarefa , usuario_atual = Depends(obter_usuario_atual)):
    response = supabase.table("tarefas").insert(tarefa.model_dump()).execute()
    return response.data[0]

#listar tarefa por id
@router.put("/{tarefa_id}")
def atualizar_tarefa(tarefa_id: str, tarefa: AtualizarTarefa, usuario_atual = Depends(obter_usuario_atual)):
    dados_atualizados = {campo: valor for campo, valor in tarefa.model_dump().items() if valor is not None}
    response = supabase.table("tarefas").update(dados_atualizados).eq("id", tarefa_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return response.data[0]

#deletar tarefa por id
@router.delete("/{tarefa_id}")
def deletar_tarefa(tarefa_id: str, usuario_atual = Depends(obter_usuario_atual)):
    response = supabase.table("tarefas").delete().eq("id", tarefa_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"Mensagem": "Tarefa deletada com sucesso"}