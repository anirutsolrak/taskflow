from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.models.tasks import CriarTarefa, AtualizarTarefa

router = APIRouter()

#listar todas as tarefas
@router.get("/")
def listar_tarefas():
    response = supabase.table("tarefas").select("*").execute()
    return response.data

#criar tarefa
@router.post("/")
def criar_tarefa(tarefa: CriarTarefa):
    response = supabase.table("tarefas").insert(tarefa.model_dump()).execute()
    return response.data[0]


@router.put("/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, tarefa: AtualizarTarefa):
    dados_atualizados = {campo: valor for campo, valor in tarefa.model_dump().items() if valor is not None}
    response = supabase.table("tarefas").update(dados_atualizados).eq("id", tarefa_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return response.data[0]

@router.delete("/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    response = supabase.table("tarefas").delete().eq("id", tarefa_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa deletada com sucesso"}