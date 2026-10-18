# Exercícios do lab (Oracle Database Free)

Base: schema `LAB`, dados fictícios de `sql/02_seed.sql`. Cada exercício tem a
**previsão** (antes de correr), a **consulta** e a **verificação**. O objetivo é o método, não só
a resposta.

## Exercício 1: total pago por distrito em 2026

**Armadilha:** a morada tem datas de vigência, e um cidadão com duas moradas faz o pagamento
aparecer duas vezes.

**Método:** linha de base na tabela de factos, depois acrescentar tabelas uma a uma, contando
linhas a cada passo.

| Passo | n (linhas) | total | Leitura |
|---|---|---|---|
| A. Pagamentos de 2026 | 132 | 7086 | Linha de base |
| B. + pedido + cidadão | 132 | 7086 | Sem mudança: FK = PK |
| C. + morada (sem vigência) | 165 | 9196 | **Fan-out**: 10 cidadãos com 2 moradas |
| D. + morada em vigor na data do pedido | 132 | 7086 | Correto |

**Consulta final (com a vigência e o `GROUP BY`):**
```sql
SELECT   d.nome AS distrito,
         COUNT(*) AS pagamentos,
         SUM(pg.valor) AS total
FROM     pagamento pg
JOIN     pedido p   ON p.id_pedido  = pg.id_pedido
JOIN     cidadao c  ON c.id_cidadao = p.id_cidadao
JOIN     morada m   ON m.id_cidadao = c.id_cidadao
                   AND p.data_submissao >= m.data_inicio_vigencia
                   AND (m.data_fim_vigencia IS NULL OR p.data_submissao <= m.data_fim_vigencia)
JOIN     servico_local sl ON sl.id_servico_local = m.id_servico_local
JOIN     distrito d       ON d.id_distrito       = sl.id_distrito
WHERE    pg.data_pagamento >= DATE '2026-01-01'
AND      pg.data_pagamento <  DATE '2027-01-01'
GROUP BY d.nome
ORDER BY d.nome;
```

**Verificação (a prova real):**
```sql
-- 1) cidadãos com mais de uma morada (onde vai haver fan-out)
SELECT id_cidadao, COUNT(*) AS moradas FROM morada GROUP BY id_cidadao HAVING COUNT(*) > 1;
-- 2) linhas contra pagamentos distintos (têm de ser iguais)
SELECT COUNT(*) AS linhas, COUNT(DISTINCT pg.id_pagamento) AS pagamentos ...;
```

**Lição:** o efeito multiplicador é o número de pagamentos ligados às chaves duplicadas,
não o número de moradas a mais.

## Exercício 2: pagamentos com valor diferente do esperado

**Previsão:** 53 pagamentos de abono (defeito do ano da submissão), nenhum de cuidador.
**Resultado:** 53 linhas, nenhum cuidador. Previsão confirmada.

```sql
SELECT pg.id_pagamento,
       pg.valor       AS valor_pago,
       ve.valor       AS valor_esperado
FROM   pagamento pg
JOIN   pedido ped
       ON ped.id_pedido = pg.id_pedido
JOIN   valor_escalao ve
       ON  ve.id_tipo_prestacao = ped.id_tipo_prestacao
       AND ve.id_escalao        = ped.id_escalao
       AND ve.ano               = EXTRACT(YEAR FROM pg.data_pagamento)
WHERE  pg.valor <> ve.valor
ORDER  BY pg.id_pagamento;
```

**Lição:** a chave da `valor_escalao` são **três** colunas (prestação, escalão, ano). Com só
o escalão, o JOIN apanha valores de outras prestações e anos.

## Exercício 3: (por fazer)
