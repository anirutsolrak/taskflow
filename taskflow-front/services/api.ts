import { Tarefa } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function buscarTarefas(): Promise<Tarefa[]> {
  const resposta = await fetch(`${API_URL}/tarefas/`)
  const dados = await resposta.json()
  if (!resposta.ok) {
    throw new Error("Erro ao buscar tarefas")
  }
  return dados
}

export async function registrar(email: string, senha: string) {
  const resposta = await fetch(`${API_URL}/auth/registro`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha }),
  })
  if (!resposta.ok) {
    throw new Error("Erro ao registrar usuário")
  }
  return resposta.json()
}

export async function login(email: string, senha: string) {
  const resposta = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha }),
  })
  if (!resposta.ok) {
    throw new Error("Email ou senha incorretos")
  }
  return resposta.json()
}
