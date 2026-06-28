from fastapi import FastAPI
from app.db.supabase import supabase
app = FastAPI()

@app.get("/")
def root():
 return {"message": "Api Funcionando correctamente"}

@app.get("/tarefas")
def tarefas():
 return [{"id": 1, "titulo": "estudo", "concluida": False}, {"id": 2, "titulo": "trabalho", "concluida": True}, {"id": 3, "titulo": "academia", "concluida": True},
        {"id": 4, "titulo": "compras", "concluida": False}, {"id": 5, "titulo": "limpeza", "concluida": True}, {"id": 6, "titulo": "cozinhar", "concluida": True}, {"id": 7, "titulo": "estudar", "concluida": False}, {"id": 8, "titulo": "trabalho", "concluida": True}, {"id": 9, "titulo": "academia", "concluida": True},]

@app.get("/status")
def status():
 return {"status": "ok", "url": str(supabase.supabase_url)}