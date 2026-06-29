import Link from "next/link";

export default function Home() {
  return (
    <main>
      <h1>Taskflow</h1>
      <p>Gerencie suas tarefas</p>
      <Link href="/login">Entrar</Link>
      <Link href="/registro">Criar conta</Link>
    </main>
  );
}
