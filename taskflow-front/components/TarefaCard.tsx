import { Tarefa } from "@/types"

interface TarefaCardProps {
  tarefa: Tarefa
}

export default function TarefaCard({ tarefa }: TarefaCardProps) {
  return (
    <div className="border rounded p-4 mb-2">
      <h3 className="font-bold">{tarefa.titulo}</h3>
      <p>{tarefa.concluida ? "Concluída" : "Pendente"}</p>
    </div>
  )
}
