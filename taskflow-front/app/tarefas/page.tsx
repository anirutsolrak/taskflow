"use client"

import TarefaCard from "@/components/TarefaCard"
import { Tarefa } from "@/types"

const tarefasFicticias: Tarefa[] = [
  { id: "1", titulo: "Estudar React", concluida: false, criado_em: "2026-06-29" },
  { id: "2", titulo: "Estudar Next.js", concluida: true, criado_em: "2026-06-29" },
]

export default function Tarefas() {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Tarefas</h1>
      {tarefasFicticias.map((tarefa) => (
        <TarefaCard key={tarefa.id} tarefa={tarefa} />
      ))}
    </main>
  )
}
