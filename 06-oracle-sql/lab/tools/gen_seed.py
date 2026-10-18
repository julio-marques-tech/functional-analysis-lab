"""Gera lab/sql/02_seed.sql: dados fictícios do Sistema de Gestão de Prestações Sociais.

Determinístico (semente fixa). Todos os dados são inventados. Esconde de propósito
casos para os exercícios: pedidos sem documentos, moradas com histórico e pagamentos
de abono com o valor do ano da submissão (o defeito estudado no playbook).

Uso (a partir da pasta lab):  python tools/gen_seed.py
"""
import datetime as dt
import random
from pathlib import Path

random.seed(42)
TODAY = dt.date(2026, 9, 30)
out = []


def q(s):
    return "'" + s.replace("'", "''") + "'"


def dd(x):
    return f"DATE '{x.isoformat()}'" if x else "NULL"


def num(x):
    return "NULL" if x is None else str(x)


def ins(table, cols, vals):
    out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(vals)});")


def rand_date(a, b):
    return a + dt.timedelta(days=random.randint(0, (b - a).days))


def first_of_month(x):
    return dt.date(x.year, x.month, 1)


def add_months(x, n):
    m = x.month - 1 + n
    return dt.date(x.year + m // 12, m % 12 + 1, 1)


# ------------------------------------------------------------------ catálogos
distritos = [(1, "Leiria"), (2, "Lisboa"), (3, "Porto"), (4, "Setúbal"), (5, "Faro")]
servicos = [
    (1, "SL-LRA", "Serviço Local de Leiria", 1),
    (2, "SL-LSB1", "Serviço Local de Lisboa Norte", 2),
    (3, "SL-LSB2", "Serviço Local de Lisboa Sul", 2),
    (4, "SL-PRT", "Serviço Local do Porto", 3),
    (5, "SL-STB", "Serviço Local de Setúbal", 4),
    (6, "SL-FAR", "Serviço Local de Faro", 5),
]
tipos_prestacao = [(1, "ABONO", "Abono de família"), (2, "CUIDADOR", "Subsídio de apoio ao cuidador")]
escaloes = [(1, "Escalão 1", 0, 3000), (2, "Escalão 2", 3000.01, 9000), (3, "Escalão 3", 9000.01, None)]
VALOR = {
    (1, 1): {2025: 50, 2026: 55}, (1, 2): {2025: 38, 2026: 40}, (1, 3): {2025: 25, 2026: 27},
    (2, 1): {2025: 120, 2026: 125}, (2, 2): {2025: 110, 2026: 115}, (2, 3): {2025: 90, 2026: 95},
}
estados = [(1, "Submetido"), (2, "Em análise"), (3, "A aguardar documentos"), (4, "Deferido"), (5, "Indeferido")]
motivos = [(1, "Rendimentos acima do limite"), (2, "Documentação insuficiente após o prazo"),
           (3, "Não reside na área de atuação")]
tipos_doc = [(1, "Comprovativo de rendimentos"), (2, "Relatório médico"), (3, "Documento de identificação")]
obrigatorios = {1: [1, 3], 2: [1, 2, 3]}

for i, n in distritos:
    ins("distrito", ["id_distrito", "nome"], [str(i), q(n)])
for i, c, n, dist in servicos:
    ins("servico_local", ["id_servico_local", "codigo", "nome", "id_distrito"], [str(i), q(c), q(n), str(dist)])
for i, c, n in tipos_prestacao:
    ins("tipo_prestacao", ["id_tipo_prestacao", "codigo", "nome"], [str(i), q(c), q(n)])
for i, n, a, b in escaloes:
    ins("escalao", ["id_escalao", "nome", "rendimento_min", "rendimento_max"], [str(i), q(n), num(a), num(b)])
for (p, e), anos in VALOR.items():
    for ano, v in anos.items():
        ins("valor_escalao", ["id_tipo_prestacao", "id_escalao", "ano", "valor"], [str(p), str(e), str(ano), str(v)])
for i, n in estados:
    ins("estado", ["id_estado", "nome"], [str(i), q(n)])
for i, n in motivos:
    ins("motivo_indeferimento", ["id_motivo", "descricao"], [str(i), q(n)])
for i, n in tipos_doc:
    ins("tipo_documento", ["id_tipo_documento", "nome"], [str(i), q(n)])
for p, docs in obrigatorios.items():
    for t in docs:
        ins("documento_obrigatorio", ["id_tipo_prestacao", "id_tipo_documento"], [str(p), str(t)])

# ------------------------------------------------------------------- técnicos
nomes = ["Ana", "Rui", "Marta", "Paulo", "Ines", "Tiago", "Carla", "Pedro", "Sofia", "Nuno", "Rita", "Hugo",
         "Joana", "Bruno", "Diana", "Andre", "Teresa", "Miguel", "Sara", "Filipe", "Helena", "Ricardo",
         "Catarina", "Jorge", "Patricia", "Daniel", "Monica", "Vasco", "Alice", "Goncalo"]
apelidos = ["Silva", "Costa", "Reis", "Neves", "Faria", "Mota", "Lima", "Santos", "Pereira", "Ferreira",
            "Almeida", "Rocha", "Marques", "Cardoso", "Correia", "Pinto", "Teixeira", "Gomes", "Ramos", "Dias"]
tecnicos = []
for i in range(1, 13):
    serv = servicos[(i - 1) % 6][0]
    nome = f"{nomes[(i * 3) % 30]} {apelidos[(i * 7) % 20]}"
    tecnicos.append((i, nome, serv))
    ins("tecnico", ["id_tecnico", "nome", "id_servico_local"], [str(i), q(nome), str(serv)])
tec_por_servico = {s[0]: [t[0] for t in tecnicos if t[2] == s[0]] for s in servicos}

# ------------------------------------------------------------------- cidadãos
ADULTS = list(range(1, 51))
CHILDREN = list(range(51, 101))
cid_nome = {}
for cid in ADULTS + CHILDREN:
    nome = f"{nomes[cid % 30]} {apelidos[(cid * 3) % 20]} {apelidos[(cid * 5 + 1) % 20]}"
    cid_nome[cid] = nome
    if cid in ADULTS:
        nasc = rand_date(dt.date(1960, 1, 1), dt.date(1996, 12, 31))
        email = f"cidadao{cid}@exemplo.pt"
        tel = "91" + str(1000000 + cid * 137)[-7:]
    else:
        nasc = rand_date(dt.date(2012, 1, 1), dt.date(2023, 12, 31))
        email = None
        tel = None
    ins("cidadao", ["id_cidadao", "niss", "nome", "data_nascimento", "nif", "email", "telemovel"],
        [str(cid), q("9" + str(cid).zfill(10)), q(nome), dd(nasc), q("999" + str(cid).zfill(6)),
         q(email) if email else "NULL", q(tel) if tel else "NULL"])

# -------------------------------------------------------------------- moradas
moradas = {}  # cid -> list of (inicio, fim, servico)
movers = set(random.sample(ADULTS, 10))
mid = 0
for cid in ADULTS:
    serv1 = random.choice(servicos)[0]
    if cid in movers:
        move = rand_date(dt.date(2025, 11, 15), dt.date(2026, 6, 30))
        serv2 = random.choice([s[0] for s in servicos if s[0] != serv1])
        ini1 = rand_date(dt.date(2019, 1, 1), dt.date(2024, 12, 31))
        moradas[cid] = [(ini1, move - dt.timedelta(days=1), serv1), (move, None, serv2)]
    else:
        moradas[cid] = [(rand_date(dt.date(2018, 1, 1), dt.date(2024, 12, 31)), None, serv1)]
    for ini, fim, serv in moradas[cid]:
        mid += 1
        ins("morada", ["id_morada", "id_cidadao", "id_servico_local", "rua", "codigo_postal", "localidade",
                       "data_inicio_vigencia", "data_fim_vigencia"],
            [str(mid), str(cid), str(serv), q(f"Rua Exemplo {cid}"), q(f"{2400 + serv}-{100 + cid}"),
             q(dict((s[0], s[2]) for s in servicos)[serv].replace("Serviço Local de ", "")), dd(ini), dd(fim)])


def servico_em(cid, data):
    for ini, fim, serv in moradas[cid]:
        if ini <= data and (fim is None or data <= fim):
            return serv
    return moradas[cid][0][2]


# --------------------------------------------------------------- dependentes
resp_principal = {}
for ch in CHILDREN:
    r = ADULTS[(ch - 51) % 25]
    resp_principal[ch] = r
    tipo = random.choice(["filho", "filho", "filha", "filha", "enteado", "neto a cargo"])
    ins("rel_dependente", ["id_cidadao_responsavel", "id_cidadao_dependente", "tipo_relacao"],
        [str(r), str(ch), q(tipo)])
    if random.random() < 0.4:
        r2 = random.choice([a for a in ADULTS if a != r])
        ins("rel_dependente", ["id_cidadao_responsavel", "id_cidadao_dependente", "tipo_relacao"],
            [str(r2), str(ch), q(tipo)])

# --------------------------------------------------------------------- pedidos
pedidos = []  # dicts


def novo_pedido(cid, prest, data_sub, forcar_deferido=False):
    p = {"id": len(pedidos) + 1, "cid": cid, "prest": prest, "sub": data_sub}
    r = random.random()
    if forcar_deferido:
        final = 4 if r < 0.7 else 2
    else:
        final = 1 if r < 0.10 else 2 if r < 0.25 else 3 if r < 0.35 else 4 if r < 0.85 else 5
    # trajetória
    path = [(1, data_sub)]
    cur = data_sub
    if final >= 2:
        cur += dt.timedelta(days=random.randint(1, 4))
        path.append((2, cur))
    if final == 3:
        cur += dt.timedelta(days=random.randint(3, 6))
        path.append((3, cur))
    if final in (4, 5):
        if random.random() < (0.3 if final == 4 else 0.4):
            cur += dt.timedelta(days=random.randint(3, 6))
            path.append((3, cur))
            cur += dt.timedelta(days=random.randint(2, 5))
            path.append((2, cur))
        cur += dt.timedelta(days=random.randint(5, 25))
        path.append((final, cur))
    # cortar o que passa de hoje
    path = [(e, d) for e, d in path if d <= TODAY]
    p["path"] = path
    p["final"] = path[-1][0]
    p["motivo"] = None
    if p["final"] == 5:
        p["motivo"] = random.choices([1, 2, 3], weights=[5, 3, 2])[0]
    p["escalao"] = None if p["final"] == 1 else random.choices([1, 2, 3], weights=[30, 45, 25])[0]
    p["deps"] = []
    pedidos.append(p)
    return p


for r in ADULTS[:25]:
    filhos = [c for c in CHILDREN if resp_principal[c] == r]
    d0 = rand_date(dt.date(2025, 10, 1), dt.date(2026, 8, 31))
    p = novo_pedido(r, 1, d0)
    p["deps"] = filhos
    if p["final"] == 5:
        d1 = p["path"][-1][1] + dt.timedelta(days=10)
        if d1 <= dt.date(2026, 9, 15):
            p2 = novo_pedido(r, 1, d1, forcar_deferido=True)
            p2["deps"] = filhos
for r in random.sample(ADULTS, 22):
    d0 = rand_date(dt.date(2025, 10, 1), dt.date(2026, 8, 31))
    novo_pedido(r, 2, d0)

for p in pedidos:
    ins("pedido", ["id_pedido", "id_cidadao", "id_tipo_prestacao", "id_escalao", "data_submissao"],
        [str(p["id"]), str(p["cid"]), str(p["prest"]), num(p["escalao"]), dd(p["sub"])])
    for ch in p["deps"]:
        ins("pedido_dependente", ["id_pedido", "id_cidadao_dependente"], [str(p["id"]), str(ch)])

# ----------------------------------------------------- histórico, atribuições
hid = 0
aid = 0
for p in pedidos:
    for est, data in p["path"]:
        hid += 1
        mot = p["motivo"] if (est == 5) else None
        obs = "Decisão registada pelo técnico" if est in (4, 5) else None
        ins("historico_estado", ["id_historico_estado", "id_pedido", "id_estado", "id_motivo", "observacao",
                                 "data_mudanca"],
            [str(hid), str(p["id"]), str(est), num(mot), q(obs) if obs else "NULL", dd(data)])
    if p["final"] >= 2:
        serv = servico_em(p["cid"], p["sub"])
        inicio = [d for e, d in p["path"] if e == 2][0]
        fim_total = p["path"][-1][1] if p["final"] in (4, 5) else None
        tecs = tec_por_servico[serv]
        t1 = random.choice(tecs)
        reatrib = len(tecs) > 1 and random.random() < 0.2 and (fim_total is None or fim_total > inicio + dt.timedelta(days=4))
        if reatrib:
            corte = inicio + dt.timedelta(days=3)
            t2 = random.choice([t for t in tecs if t != t1])
            segmentos = [(t1, inicio, corte), (t2, corte + dt.timedelta(days=1), fim_total)]
        else:
            segmentos = [(t1, inicio, fim_total)]
        for t, a, b in segmentos:
            aid += 1
            ins("atribuicao", ["id_atribuicao", "id_pedido", "id_tecnico", "data_inicio", "data_fim"],
                [str(aid), str(p["id"]), str(t), dd(a), dd(b)])

# ------------------------------------------------------------------ documentos
did = 0
for p in pedidos:
    req = list(obrigatorios[p["prest"]])
    if p["final"] == 1:
        entregues = []
    elif p["final"] == 3 or (p["final"] == 5 and p["motivo"] == 2):
        entregues = req[:]
        entregues.remove(random.choice(req))
    else:
        entregues = req
    for t in entregues:
        did += 1
        ins("documento", ["id_documento", "id_pedido", "id_tipo_documento", "data_entrega", "ficheiro"],
            [str(did), str(p["id"]), str(t), dd(p["sub"] + dt.timedelta(days=random.randint(0, 3))),
             q(f"/docs/{p['id']}/{t}.pdf")])

# ------------------------------------------------------- contas e pagamentos
cid_conta = 0
pid = 0
buggy = 0
for p in pedidos:
    if p["final"] != 4:
        continue
    decisao = p["path"][-1][1]
    contas = []
    cid_conta += 1
    iban = "PT50" + "0000" + "".join(str(random.randint(0, 9)) for _ in range(17))
    muda = decisao + dt.timedelta(days=random.randint(20, 150))
    if random.random() < 0.25 and muda <= TODAY:
        contas.append((cid_conta, iban, decisao, muda - dt.timedelta(days=1)))
        cid_conta += 1
        iban2 = "PT50" + "0000" + "".join(str(random.randint(0, 9)) for _ in range(17))
        contas.append((cid_conta, iban2, muda, None))
    else:
        contas.append((cid_conta, iban, decisao, None))
    for c, ib, a, b in contas:
        ins("conta_bancaria", ["id_conta", "id_pedido", "iban", "data_inicio_vigencia", "data_fim_vigencia"],
            [str(c), str(p["id"]), q(ib), dd(a), dd(b)])
    mes = add_months(first_of_month(decisao), 1)
    while mes <= dt.date(2026, 9, 1):
        data_pag = dt.date(mes.year, mes.month, 5)
        conta = [c for c, ib, a, b in contas if a <= data_pag and (b is None or data_pag <= b)]
        conta = conta[0] if conta else contas[-1][0]
        ano_correto = data_pag.year
        valor = VALOR[(p["prest"], p["escalao"])][ano_correto]
        if p["prest"] == 1 and p["sub"].year == 2025 and data_pag.year == 2026:
            valor = VALOR[(p["prest"], p["escalao"])][2025]  # defeito: ano da submissão
            if valor != VALOR[(p["prest"], p["escalao"])][2026]:
                buggy += 1
        pid += 1
        ins("pagamento", ["id_pagamento", "id_pedido", "id_conta", "mes_referencia", "valor", "data_pagamento"],
            [str(pid), str(p["id"]), str(conta), dd(mes), str(valor), dd(data_pag)])
        mes = add_months(mes, 1)

out.append("COMMIT;")
dest = Path(__file__).resolve().parent.parent / "sql" / "02_seed.sql"
header = ("-- Dados fictícios (gerados por tools/gen_seed.py, semente fixa). Executar com Alt+X no DBeaver.\n"
          "-- Esconde de propósito: pedidos sem documentos, moradas com histórico, e pagamentos\n"
          "-- de abono com o valor do ano da submissão (defeito do playbook).\n")
dest.write_text(header + "\n".join(out) + "\n", encoding="utf-8")
print(f"escrito {dest} com {len(out)} instruções")
print(f"pedidos={len(pedidos)} pagamentos={pid} pagamentos_com_valor_do_ano_errado={buggy}")
