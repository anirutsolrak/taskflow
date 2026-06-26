from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
 return {"message": "Api Funcionando correctamente"}

@app.get("/tarefas")
def tarefas():
 return {"tarefas urgentes": ["tarefa 1", "tarefa 2", "tarefa 3"], "tarefas normais": ["tarefa 4", "tarefa 5", "tarefa 6"]}