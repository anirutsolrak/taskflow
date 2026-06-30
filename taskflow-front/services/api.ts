import { Tarefa } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL

function getToken(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem("access_token")
}

export async function buscarTarefas(): Promise<Tarefa[]> {
  const token = getToken()
  const resposta = await fetch(`${API_URL}/tarefas/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!resposta.ok) {
    throw new Error("Erro ao buscar tarefas")
  }
  return resposta.json()
}

export async function criarTarefa(titulo: string): Promise<Tarefa> {
  const token = getToken()
  const resposta = await fetch(`${API_URL}/tarefas/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ titulo }),
  })
  if (!resposta.ok) {
    throw new Error("Erro ao criar tarefa")
  }
  return resposta.json()
}

export async function atualizarTarefa(id: string, concluida: boolean): Promise<Tarefa> {
  const token = getToken()
  const resposta = await fetch(`${API_URL}/tarefas/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ concluida }),
  })
  if (!resposta.ok) {
    throw new Error("Erro ao atualizar tarefa")
  }
  return resposta.json()
}

export async function deletarTarefa(id: string): Promise<void> {
  const token = getToken()
  const resposta = await fetch(`${API_URL}/tarefas/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!resposta.ok) {
    throw new Error("Erro ao deletar tarefa")
  }
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
