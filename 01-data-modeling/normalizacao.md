# Normalização: da folha de cálculo à 3FN e FNBC

> Aplicada à [folha de cálculo atual](../case-study/folha-pedidos-atual.md) do caso de estudo.
> Cada secção termina com a forma de o explicar numa conversa técnica.

## Porquê normalizar

Para que **cada facto fique guardado num só sítio**: quando muda, muda uma vez, e nunca há
duas versões a contradizer-se. A normalização elimina três **anomalias**:

| Anomalia | O que é | Na folha |
|---|---|---|
| **Atualização** | O mesmo facto está em várias linhas e uma fica desatualizada | O telemóvel do João Reis é 913000222 no P-1002 e 919999999 no P-1005 |
| **Inserção** | Não se consegue guardar um facto sem outro | Não se consegue registar um técnico que ainda não tenha pedidos |
| **Remoção** | Apagar um registo destrói informação que se queria manter | Apagar o P-1004 apaga a única informação de que a Carla Mota existe |

> **Na entrevista:** "Normalizo para eliminar a redundância e as três anomalias: de
> atualização, de inserção e de remoção. Sempre que identifico uma violação de uma forma
> normal, digo qual anomalia ela causa."

## Dependência funcional: a base de tudo

**X → Y** ("X determina Y"): sempre que X tem o mesmo valor, Y também tem o mesmo valor.

**Teste com os dados:** procurar valores repetidos de X e ver se Y se repete sempre igual.
**Basta um contraexemplo para invalidar a dependência.**

| Dependência | Verificação na folha |
|---|---|
| NISS → nome, telemóvel | 11111111111 é sempre "Ana Silva" |
| NISS ↛ serviço local | 44444444444 aparece com SL-LRA e com SL-LSB (contraexemplo) |
| NISS ↛ estado | 11111111111 aparece "Em análise" e "Submetido" (contraexemplo) |
| prestação → valor base | Abono é sempre 50,00; cuidador é sempre 120,00 |
| técnico → serviço local | Marta Costa é sempre SL-LRA |
| serviço local → distrito | SL-LRA é sempre Leiria |

## 1FN: valores atómicos, sem grupos repetidos

**Violação:** a coluna "Dependentes" tem **vários valores** (separados por `;`) e cada um
**não é atómico** (`NISS - nome` junta dois dados).

**Correção:** o atributo multivalorado sai para uma tabela própria, uma linha por valor, com a
chave da tabela de origem. Como a coluna está na linha do pedido, a tabela é
**PEDIDO_DEPENDENTE** (dependentes incluídos em cada pedido), com chave composta
(n.º pedido, NISS dependente).

**Solução errada:** colunas `dependente_1`, `dependente_2`, `dependente_3`. É um grupo
repetido e também viola a 1FN.

> **Na entrevista:** "A 1FN exige valores atómicos e nenhum grupo repetido. Um atributo
> multivalorado sai para uma tabela própria, uma linha por valor, que leva a chave da tabela
> de origem como chave estrangeira."

## 2FN: sem dependências parciais

Só se aplica a tabelas com **chave composta**. Nenhum atributo não-chave pode depender de
**parte** da chave.

**Violação:** em PEDIDO_DEPENDENTE (n.º pedido, NISS dependente, nome dependente), o nome
depende só do NISS. O nome do mesmo dependente ficaria repetido em cada pedido em que
aparece (anomalia de atualização), não poderia existir sem pedido (inserção) e perder-se-ia
ao apagar o pedido (remoção).

**Correção:** o nome vai para CIDADAO (o dependente é um cidadão). PEDIDO_DEPENDENTE fica só
com a chave composta: uma tabela associativa pura.

> **Na entrevista:** "A 2FN só se aplica com chave composta: nenhum atributo pode depender só
> de parte da chave. Uma tabela com chave simples, se já está em 1FN, está automaticamente em
> 2FN."

## 3FN: sem dependências transitivas

Nenhum atributo não-chave pode depender de outro atributo não-chave. Cada atributo depende
**da chave, de toda a chave, e de nada mais do que a chave**.

**Violações na tabela PEDIDO:**

```
n.º pedido → NISS → nome, telemóvel
n.º pedido → prestação → valor base
n.º pedido → técnico → serviço local → distrito
```

**Resultado em 3FN:**

| Tabela | Colunas (chave a **negrito**) |
|---|---|
| CIDADAO | **NISS**, nome, telemóvel |
| TIPO_PRESTACAO | **prestação**, valor base |
| TECNICO | **técnico**, serviço local (FK) |
| SERVICO_LOCAL | **serviço local**, distrito |
| PEDIDO | **n.º pedido**, NISS (FK), prestação (FK), técnico (FK), estado, data |
| PEDIDO_DEPENDENTE | **n.º pedido**, **NISS dependente** |

O estado e a data ficam no PEDIDO porque dependem apenas da chave: nenhuma outra coluna os
determina (contraexemplos na tabela de dependências).

**Validação cruzada:** as tabelas obtidas são as mesmas entidades do
[DER conceptual](der-conceptual.md). A entrevista dá o modelo de cima para baixo; a
normalização dá-o de baixo para cima, a partir dos dados.

**Qualidade de dados:** ao normalizar dados existentes aparecem conflitos (o telemóvel do João
com dois valores). A tabela normalizada só aceita um; qual fica decide-se com o negócio,
antes da migração.

> **Na entrevista:** "A 3FN elimina dependências transitivas. Identifico-as testando com os
> dados: se sempre que X se repete Y se repete igual, X determina Y, e Y sai para uma tabela
> própria com X como chave. Ao normalizar dados reais surgem conflitos que se resolvem com o
> negócio antes da migração."

## FNBC (Boyce-Codd): todo o determinante é chave candidata

Versão mais rigorosa da 3FN. Só difere quando há chaves candidatas compostas que se
sobrepõem.

**Exemplo:** se cada técnico fosse especialista numa só prestação, a tabela
ANALISE (cidadão, prestação, técnico) teria:

- (cidadão, prestação) → técnico — a chave
- técnico → prestação — o **técnico** é determinante mas **não é chave**

O facto "este técnico trata desta prestação" repete-se em cada linha em que o técnico aparece
(anomalia de atualização). A tabela cumpre a 3FN (a prestação faz parte da chave) mas falha a
FNBC. Correção: TECNICO (técnico, prestação) + ANALISE (cidadão, técnico).

> **Na entrevista:** "A FNBC exige que todo o determinante seja chave candidata. Na prática,
> um modelo em 3FN quase sempre está em FNBC; só diferem com chaves candidatas compostas que
> se sobrepõem."

## Desnormalização

Juntar ou duplicar dados **de propósito**, por uma razão concreta (normalmente desempenho de
leitura). Só se desnormaliza o que já foi normalizado.

| Situação | Decisão | Razão |
|---|---|---|
| Estado atual mostrado centenas de vezes por dia na lista dos técnicos | Desnormalizar: `estado_atual` no PEDIDO | Leitura muito frequente; manter sincronizado na mesma transação que o histórico, depois de confirmar que um índice não chega |
| Nome do distrito em cada pedido "para evitar um JOIN" | Não desnormalizar | Um JOIN a uma tabela pequena com índice é barato; duplicar recria a dependência transitiva |
| Total pago por distrito e prestação, consultado uma vez por mês | Não desnormalizar o sistema transacional | Usar uma view, uma materialized view ou a camada de BI / data warehouse |
| Valor efetivamente pago guardado no PAGAMENTO | Correto guardar | É um registo histórico do que se pagou, mesmo que a tabela de valores seja corrigida depois |

**Alternativas antes de desnormalizar:** índices, views, materialized views (Oracle).

> **Na entrevista:** "No sistema transacional normalizo até à 3FN. Desnormalizo só por uma
> razão concreta e medida, com um mecanismo que mantenha as cópias sincronizadas, e considero
> antes índices ou materialized views. No data warehouse é ao contrário: o modelo em estrela é
> desnormalizado de propósito, porque o objetivo é consultar depressa."
