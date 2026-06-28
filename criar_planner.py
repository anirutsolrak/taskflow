import msal
import requests
import json
from datetime import datetime, timedelta, timezone

# ── CONFIG ────────────────────────────────────────────────────────────────
CLIENT_ID = "37f64015-d93b-4840-ac56-9e857149a10e"
SCOPES = ["Tasks.ReadWrite", "Group.ReadWrite.All", "User.Read"]

# ── AUTH ──────────────────────────────────────────────────────────────────
app = msal.PublicClientApplication(CLIENT_ID, authority="https://login.microsoftonline.com/common")
flow = app.initiate_device_flow(scopes=SCOPES)
print(flow["message"])
result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result:
    print("Erro ao obter token:", result.get("error_description"))
    exit()

TOKEN = result["access_token"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def graph(method, url, body=None):
    r = requests.request(method, f"https://graph.microsoft.com/v1.0{url}", headers=HEADERS, json=body)
    if not r.ok:
        print(f"Erro {r.status_code} em {url}: {r.text}")
        return None
    return r.json() if r.text else {}

# ── USER ID ───────────────────────────────────────────────────────────────
me = graph("GET", "/me")
user_id = me["id"]
user_email = me.get("userPrincipalName", "")
print(f"\n✅ Logado como: {me.get('displayName')} ({user_email})")

# ── CRIAR GRUPO (necessário pro Planner) ─────────────────────────────────
print("\n⏳ Criando grupo no Microsoft 365...")
grupo = graph("POST", "/groups", {
    "displayName": "Demo — Deliberações de Assembleia",
    "mailNickname": "demo-deliberacoes",
    "groupTypes": ["Unified"],
    "mailEnabled": True,
    "securityEnabled": False,
    "visibility": "Private"
})

if not grupo:
    print("Falha ao criar grupo.")
    exit()

group_id = grupo["id"]
print(f"✅ Grupo criado: {group_id}")

# Adicionar o usuário como owner (às vezes demora um pouco)
import time
time.sleep(3)
graph("POST", f"/groups/{group_id}/owners/$ref", {
    "@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"
})
graph("POST", f"/groups/{group_id}/members/$ref", {
    "@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"
})
print("✅ Usuário adicionado ao grupo")

# ── CRIAR PLANNER ─────────────────────────────────────────────────────────
time.sleep(5)  # grupo precisa propagar
print("\n⏳ Criando plano no Planner...")
plano = graph("POST", "/planner/plans", {
    "owner": group_id,
    "title": "Deliberações de Assembleia — Demo"
})

if not plano:
    print("Falha ao criar plano. Tente novamente em 1 minuto (o grupo precisa propagar).")
    exit()

plan_id = plano["id"]
print(f"✅ Plano criado: {plan_id}")
time.sleep(2)

# ── CRIAR BUCKETS — GRUPO 1: POR STATUS ──────────────────────────────────
print("\n⏳ Criando buckets por status...")
buckets_status = {}
for nome in ["📋 Pendente", "🔄 Em Andamento", "✅ Concluído", "🚨 Atrasado"]:
    b = graph("POST", "/planner/buckets", {"name": nome, "planId": plan_id, "orderHint": " !"})
    if b:
        buckets_status[nome] = b["id"]
        print(f"  ✅ {nome}")
    time.sleep(1)

# ── CRIAR BUCKETS — GRUPO 2: POR SETOR ───────────────────────────────────
print("\n⏳ Criando buckets por setor...")
buckets_setor = {}
for nome in ["💰 Financeiro", "⚙️ Operacional", "🔧 Manutenção", "📄 Jurídico"]:
    b = graph("POST", "/planner/buckets", {"name": nome, "planId": plan_id, "orderHint": " !"})
    if b:
        buckets_setor[nome] = b["id"]
        print(f"  ✅ {nome}")
    time.sleep(1)

# ── DATAS ─────────────────────────────────────────────────────────────────
hoje = datetime.now(timezone.utc)
def prazo(dias):
    return (hoje + timedelta(days=dias)).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── TAREFAS ───────────────────────────────────────────────────────────────
# 4 tarefas nos buckets de status + 4 nos buckets de setor
tarefas = [
    # Bucket status
    {
        "title": "Solicitar orçamento — pintura fachada Cond. A",
        "bucket": "📋 Pendente",
        "due": prazo(7),
        "notes": "Deliberação AGO 10/06/2026 — mínimo 3 orçamentos"
    },
    {
        "title": "Contratar empresa de dedetização — Cond. B",
        "bucket": "🔄 Em Andamento",
        "due": prazo(3),
        "notes": "Deliberação AGE 05/06/2026 — urgente, prazo curto"
    },
    {
        "title": "Revisar contrato de seguro coletivo",
        "bucket": "✅ Concluído",
        "due": prazo(-2),
        "notes": "Deliberação AGO 01/06/2026 — concluído em 20/06"
    },
    {
        "title": "Instalar câmeras no estacionamento — Cond. C",
        "bucket": "🚨 Atrasado",
        "due": prazo(-5),
        "notes": "Deliberação AGE 28/05/2026 — prazo vencido sem conclusão"
    },
    # Bucket setor
    {
        "title": "Atualizar previsão orçamentária — Cond. A",
        "bucket": "💰 Financeiro",
        "due": prazo(10),
        "notes": "Deliberação AGO 10/06/2026 — enviar ao síndico até o prazo"
    },
    {
        "title": "Regularizar alvará de funcionamento — Cond. B",
        "bucket": "📄 Jurídico",
        "due": prazo(14),
        "notes": "Deliberação AGE 05/06/2026 — acionar escritório parceiro"
    },
    {
        "title": "Agendar vistoria elétrica — Cond. C",
        "bucket": "🔧 Manutenção",
        "due": prazo(5),
        "notes": "Deliberação AGO 10/06/2026 — empresa já aprovada pelo síndico"
    },
    {
        "title": "Emitir relatório de inadimplência — Cond. A",
        "bucket": "⚙️ Operacional",
        "due": prazo(2),
        "notes": "Deliberação AGE 12/06/2026 — enviar por e-mail aos condôminos"
    },
]

print("\n⏳ Criando tarefas...")
todos_buckets = {**buckets_status, **buckets_setor}

for t in tarefas:
    bucket_id = todos_buckets.get(t["bucket"])
    if not bucket_id:
        print(f"  ⚠️ Bucket não encontrado: {t['bucket']}")
        continue

    tarefa = graph("POST", "/planner/tasks", {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": t["title"],
        "dueDateTime": t["due"],
        "assignments": {
            user_id: {
                "@odata.type": "microsoft.graph.plannerAssignment",
                "orderHint": " !"
            }
        }
    })

    if tarefa:
        # Adicionar nota na tarefa
        etag = tarefa.get("@odata.etag", "")
        task_id = tarefa["id"]
        time.sleep(1)
        details = graph("GET", f"/planner/tasks/{task_id}/details")
        if details:
            graph("PATCH", f"/planner/tasks/{task_id}/details", {
                "description": t["notes"]
            })
        print(f"  ✅ {t['title']}")
    time.sleep(1)

# ── LINK FINAL ────────────────────────────────────────────────────────────
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PLANNER DE DEMONSTRAÇÃO CRIADO COM SUCESSO!

Acesse em:
https://tasks.office.com/

Ou direto pelo link do plano:
https://tasks.office.com/Home/Planner/#/plantaskboard?groupId={group_id}&planId={plan_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")