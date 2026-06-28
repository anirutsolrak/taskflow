from fastapi import FastAPI
from app.db.supabase import supabase
from app.routers.tasks import router as task_router

app = FastAPI()
app.include_router(task_router, prefix ="/tarefas", tags=["Tarefas"])
@app.get("/")
def root():
 return {"message": "Api Funcionando corretamente"}

@app.get("/status")
def status():
 return {"status": "Ok", "url": str(supabase.supabase_url)}