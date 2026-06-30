"use client"

import { useState, useEffect } from "react"
import TarefaCard from "@/components/TarefaCard"
import { buscarTarefas } from "@/services/api"
import { Tarefa } from "@/types"

export default function Tarefas() {
  const [tarefas, setTarefas] = useState<Tarefa[]>([])
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    async function carregarTarefas() {
      try {
      const dados = await buscarTarefas()
      setTarefas(dados)
    } catch { setTarefas([])}
    finally {
      setCarregando(false)
    }
  }
    carregarTarefas()
  }, [])

  if (carregando) {
    return <p className="p-8">Carregando tarefas...</p>
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Tarefas</h1>
      {tarefas.map((tarefa) => (
        <TarefaCard key={tarefa.id} tarefa={tarefa} />
      ))}
    </main>
  )
}
