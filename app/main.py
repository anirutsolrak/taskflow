from fastapi import FastAPI
from app.db.supabase import supabase
from app.routers.tasks import router as task_router
from app.routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(task_router, prefix ="/tarefas", tags=["Tarefas"])
app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])



@app.get("/")
def root():
 return {"message": "Api Funcionando corretamente"}

@app.get("/status")
def status():
 return {"status": "Ok", "url": str(supabase.supabase_url)}