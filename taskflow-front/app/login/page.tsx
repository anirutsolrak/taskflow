"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { login } from "@/services/api"

export default function Login() {
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")
  const [erro, setErro] = useState("")
  const router = useRouter()

  async function handleSubmit(evento: React.FormEvent) {
    evento.preventDefault()
    setErro("")
    try {
      const dados = await login(email, senha)
      localStorage.setItem("access_token", dados.access_token)
      router.push("/tarefas")
    } catch (erroCapturado) {
      setErro("Email ou senha incorretos")
    }
  }

  return (
    <main className="p-8 max-w-sm mx-auto">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 rounded"
          required
        />
        <input
          type="password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          className="border p-2 rounded"
          required
        />
        {erro && <p className="text-red-500">{erro}</p>}
        <button type="submit" className="bg-black text-white p-2 rounded">
          Entrar
        </button>
      </form>
    </main>
  )
}
