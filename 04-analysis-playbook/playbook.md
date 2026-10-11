# Playbook de análise: como abordar um problema vago

> Método para transformar um pedido do tipo *"os cidadãos queixam-se de que demoram muito"* ou
> *"há pagamentos com valores errados"* numa análise ordenada. Aplicado ao
> [caso de estudo](../case-study/) e ao modelo de dados dos módulos 01 e 02.

## Os sete passos

| # | Passo | Perguntas-chave |
|---|---|---|
| 1 | **Clarificar o problema e o sucesso** | O que é "muito", comparado com quê? Há um prazo-alvo? Desde quando? Em que prestações e distritos? Como saberemos que está resolvido? |
| 2 | **Contexto e pessoas** | Quem é afetado? Quem sabe como funciona? Entrevistas e observação |
| 3 | **Medir o AS-IS com dados** | Tempo por estado, por prestação, por distrito, por técnico. Onde está a maior fatia? (Pareto) |
| 4 | **Mapear o processo real** | Seguir casos reais de ponta a ponta; desenhar o processo com as esperas (BPMN) |
| 5 | **Causa raiz** | "5 porquês", diagrama de causa e efeito; separar causas de **processo**, **pessoas**, **sistema** e **dados** |
| 6 | **Opções e prioridades** | Vitórias rápidas vs mudanças estruturais; valor × esforço, MoSCoW |
| 7 | **Especificar, validar e medir** | Requisitos e critérios de aceitação; cenários de teste; validar com o negócio; medir contra a linha de base |

## As três lentes

Cada frase ouvida numa entrevista vai para uma de três colunas:

| Dados | Comportamento | Regras |
|---|---|---|
| O que se guarda (substantivos) | O que o sistema faz (verbos, fluxos, estados) | O que é permitido ou proibido ("só pode", "não pode") |
| → Modelo de dados | → Casos de uso, BPMN, diagrama de estados, ecrãs | → Restrições ou regras de negócio |

A mesma frase pode alimentar duas colunas. O erro é pôr comportamento dentro do modelo de dados.

## Como gerar perguntas: sete palavras

| Palavra | O que descobres |
|---|---|
| **Quem** | Quem é afetado, quem se queixa, quem sabe |
| **O quê** | O que acontece exatamente; um exemplo concreto |
| **Onde** | Em que parte, canal ou sistema |
| **Quando** | Desde quando; sempre ou às vezes |
| **Quanto** | Quantos casos; que percentagem |
| **Porquê agora** | O que mudou; porque é prioritário |
| **Sucesso** | Como se sabe que está resolvido |

Ouvir o que já foi dito também conta: se o pedido diz "desde que entrou o sistema novo", a
pergunta útil não é *desde quando*, é *começou exatamente com o sistema novo, ou já havia casos
antes?* (regressão ou problema que passou a ser visível).

## Quando o problema está ativo: contenção primeiro

| Momento | Pergunta |
|---|---|
| **Contenção** | Como paramos o problema já? (ex.: suspender o próximo lote de pagamentos) |
| **Correção** | Como corrigimos o que já aconteceu? |
| **Causa raiz** | O que falhou, para não voltar a acontecer? |

O sucesso inclui regularizar as pessoas afetadas, e não só deixar de errar.

## Hipóteses ligadas ao modelo

Cada hipótese aponta para uma parte do modelo e tem um teste simples nos dados:

| Hipótese | Onde olhar | Teste |
|---|---|---|
| Valores desatualizados ou em falta | `VALOR_ESCALAO` | Existe linha para o ano em causa? O valor bate com a tabela aprovada? |
| Intervalos ou valores alterados à mão | `ESCALAO`, `VALOR_ESCALAO` | Quem alterou e quando (colunas de auditoria do transacional)? |
| Escalão atribuído errado | `PEDIDO.id_escalao` | Distribuição de escalões antes e depois da data do problema |
| Regra ambígua (que ano conta?) | Regras de negócio | Pedidos submetidos num ano e pagos no seguinte |
| Falha de migração ou de carga | Dados de origem vs destino | Reconciliação de contagens e totais |

**Teste para encontrar pagamentos com valor diferente do esperado:**

```sql
SELECT pg.id_pagamento, pg.valor AS valor_pago, ve.valor AS valor_esperado
FROM   pagamento pg
JOIN   pedido ped        ON ped.id_pedido = pg.id_pedido
JOIN   valor_escalao ve  ON ve.id_tipo_prestacao = ped.id_tipo_prestacao
                        AND ve.id_escalao        = ped.id_escalao
                        AND ve.ano               = EXTRACT(YEAR FROM pg.data_pagamento)
WHERE  pg.valor <> ve.valor;
```

O **JOIN encontra a linha esperada**, pela chave. O **WHERE faz o julgamento**. Pôr a
comparação dos valores no JOIN anula a consulta (devolve zero linhas).

## Da causa raiz ao teste executável

Se a causa for a regra do ano (o sistema usa o ano da submissão, o negócio esperava o do
pagamento), o cenário que teria apanhado o erro é um **exemplo com números** em que a resposta
certa e a errada dão resultados diferentes:

```gherkin
Funcionalidade: Valor dos pagamentos

  Contexto:
    Dado que o valor do abono de família, no escalão 2, é 38,00 € em 2025 e 40,00 € em 2026

  Esquema do Cenário: O valor do pagamento é o do ano em que é efetuado
    Dado um pedido de abono, escalão 2, submetido em <submissao>
    Quando é processado o pagamento de <pagamento>
    Então o valor do pagamento é <valor> €

    Exemplos:
      | submissao     | pagamento     | valor |
      | dezembro 2025 | dezembro 2025 | 38,00 |
      | dezembro 2025 | janeiro 2026  | 40,00 |
      | janeiro 2026  | janeiro 2026  | 40,00 |
```

**Teste de um bom cenário:** *falharia no sistema com o defeito?* O `Então` afirma um
resultado observável (o valor), não o mecanismo ("o sistema considera o ano"). As linhas dos
extremos protegem o caso oposto e o caso normal (valores-limite).

## Exemplo completo: "demoram muito a responder"

1. **Clarificar:** o que é "muito"? Prazo-alvo? Em que prestações? Distinguir *sistema lento*
   de *processo lento*.
2. **Pessoas:** técnicos e coordenadora; onde sentem que o pedido encalha.
3. **Medir:** com `HISTORICO_ESTADO`, tempo que cada pedido passa em cada estado. Provável
   maior fatia: "A aguardar documentos" (um problema de processo, não de base de dados).
4. **Mapear:** seguir alguns pedidos reais; BPMN com as esperas.
5. **Causa raiz:** 5 porquês sobre o estado dominante; separar processo, pessoas, sistema, dados.
6. **Opções:** lembretes automáticos de documentos em falta (vitória rápida); redistribuir
   carga; rever a lista de documentos obrigatórios (estrutural). Priorizar por valor e esforço.
7. **Especificar e medir:** histórias com critérios de aceitação e cenários; medir o tempo
   médio por estado antes e depois.

## Como dizê-lo

> "Antes de propor qualquer solução, clarifico o problema com quem o levanta: o que é 'muito',
> qual o prazo esperado, em que prestações. Depois meço: com o histórico de estados vejo onde
> se perde o tempo. Sigo alguns casos reais de ponta a ponta e converso com quem os trata, para
> perceber o processo como realmente acontece. Com isso procuro a causa raiz, que pode ser de
> processo, de pessoas ou de sistema, e só então proponho opções, priorizo e defino os
> requisitos. No fim, meço o resultado contra a linha de base."

> "Se o problema está ativo, a primeira prioridade é a contenção, para não aumentar o dano.
> Só depois investigo a causa e planeio a correção do que já aconteceu."
