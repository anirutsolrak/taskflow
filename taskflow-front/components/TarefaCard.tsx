import { Tarefa } from "@/types"

interface TarefaCardProps {
  tarefa: Tarefa
  aoAlternar: (id: string, concluida: boolean) => void
  aoDeletar: (id: string) => void
}

export default function TarefaCard({ tarefa, aoAlternar, aoDeletar }: TarefaCardProps) {
  return (
    <div className="border rounded p-4 mb-2 flex justify-between items-center">
      <div>
        <h3 className="font-bold">{tarefa.titulo}</h3>
        <p>{tarefa.concluida ? "Concluída" : "Pendente"}</p>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => aoAlternar(tarefa.id, !tarefa.concluida)}
          className="bg-blue-500 text-white px-3 py-1 rounded"
        >
          {tarefa.concluida ? "Reabrir" : "Concluir"}
        </button>
        <button
          onClick={() => aoDeletar(tarefa.id)}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Deletar
        </button>
      </div>
    </div>
  )
}
