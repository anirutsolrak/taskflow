"use client"

import { useState, useEffect } from "react"
import TarefaCard from "@/components/TarefaCard"
import { buscarTarefas, criarTarefa, atualizarTarefa, deletarTarefa } from "@/services/api"
import { Tarefa } from "@/types"

export default function Tarefas() {
  const [tarefas, setTarefas] = useState<Tarefa[]>([])
  const [carregando, setCarregando] = useState(true)
  const [novoTitulo, setNovoTitulo] = useState("")

  async function carregarTarefas() {
    try {
      const dados = await buscarTarefas()
      setTarefas(dados)
    } catch {
      setTarefas([])
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    carregarTarefas()
  }, [])

  async function handleCriar(evento: React.FormEvent) {
    evento.preventDefault()
    if (!novoTitulo.trim()) return
    await criarTarefa(novoTitulo)
    setNovoTitulo("")
    carregarTarefas()
  }

  async function handleAlternar(id: string, concluida: boolean) {
    await atualizarTarefa(id, concluida)
    carregarTarefas()
  }

  async function handleDeletar(id: string) {
    await deletarTarefa(id)
    carregarTarefas()
  }

  if (carregando) {
    return <p className="p-8">Carregando tarefas...</p>
  }

  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Tarefas</h1>
      <form onSubmit={handleCriar} className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Nova tarefa"
          value={novoTitulo}
          onChange={(e) => setNovoTitulo(e.target.value)}
          className="border p-2 rounded flex-1"
        />
        <button type="submit" className="bg-black text-white px-4 rounded">
          Adicionar
        </button>
      </form>
      {tarefas.map((tarefa) => (
        <TarefaCard
          key={tarefa.id}
          tarefa={tarefa}
          aoAlternar={handleAlternar}
          aoDeletar={handleDeletar}
        />
      ))}
    </main>
  )
}
