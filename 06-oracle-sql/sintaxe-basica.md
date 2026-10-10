# SQL em Oracle: sintaxe básica de cor

> Folha de treino com tabelas do [caso de estudo](../case-study/). Para treinar: tapar a
> solução e escrever de memória.

## Tipos de dados mais usados

| Tipo | Para quê |
|---|---|
| `VARCHAR2(n)` | Texto de tamanho variável (**o tamanho é obrigatório**) |
| `NUMBER(p, s)` | Números (`NUMBER(10)` inteiro; `NUMBER(10,2)` com 2 casas decimais) |
| `DATE` | Data **e hora** (segundos) |
| `TIMESTAMP` | Data e hora com frações de segundo |
| `CLOB` / `BLOB` | Texto grande / conteúdo binário (ex.: um XML completo) |

## DDL: criar e alterar estruturas

```sql
CREATE TABLE servico_local (
    codigo   NUMBER(10)    PRIMARY KEY,
    nome     VARCHAR2(100) NOT NULL,
    distrito VARCHAR2(50)  NOT NULL
);

CREATE TABLE tecnico (
    id          NUMBER(10)    PRIMARY KEY,
    nome        VARCHAR2(100) NOT NULL,
    cod_servico NUMBER(10)    NOT NULL REFERENCES servico_local (codigo)
);
```

A chave estrangeira com nome (útil para mensagens de erro e para a gerir depois):

```sql
CREATE TABLE pedido (
    n_pedido       NUMBER(10)   PRIMARY KEY,
    id_cidadao     NUMBER(10)   NOT NULL,
    estado         VARCHAR2(30) DEFAULT 'Submetido' NOT NULL,
    data_submissao DATE         DEFAULT SYSDATE NOT NULL,
    CONSTRAINT fk_pedido_cidadao FOREIGN KEY (id_cidadao) REFERENCES cidadao (id_cidadao),
    CONSTRAINT ck_pedido_estado  CHECK (estado IN ('Submetido','Em análise','Deferido','Indeferido'))
);
```

| Restrição | Faz |
|---|---|
| `PRIMARY KEY` | Identifica a linha: única e nunca nula |
| `FOREIGN KEY ... REFERENCES` | Garante que o valor existe na tabela referenciada |
| `NOT NULL` | A coluna não pode ficar vazia |
| `UNIQUE` | Não admite valores repetidos (ex.: o NISS) |
| `CHECK` | Valida uma condição |
| `DEFAULT` | Valor usado quando não se indica nenhum |

**Chave gerada automaticamente (Oracle 12c ou superior):**

```sql
id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
```

Antes do 12c usava-se uma **sequence** (`CREATE SEQUENCE seq_pedido;` e `seq_pedido.NEXTVAL`).

```sql
ALTER TABLE tecnico ADD (email VARCHAR2(100));              -- acrescentar coluna
ALTER TABLE tecnico MODIFY (nome VARCHAR2(150));            -- alterar tipo ou tamanho
ALTER TABLE tecnico DROP COLUMN email;                      -- remover coluna
ALTER TABLE tecnico ADD CONSTRAINT uk_tecnico_nome UNIQUE (nome);
DROP TABLE tecnico;                                         -- apagar a tabela
```

## DML: inserir, alterar e apagar dados

```sql
INSERT INTO servico_local (codigo, nome, distrito)
VALUES (1, 'Serviço Local de Leiria', 'Leiria');

UPDATE pedido SET estado = 'Em análise' WHERE n_pedido = 1001;

DELETE FROM pedido WHERE n_pedido = 1001;

COMMIT;      -- torna as alterações definitivas
ROLLBACK;    -- desfaz tudo desde o último COMMIT
```

- **Texto e datas** levam aspas simples: `'Leiria'`; uma data: `DATE '2026-03-02'` ou
  `TO_DATE('2026-03-02', 'YYYY-MM-DD')`.
- **`UPDATE` e `DELETE` sem `WHERE` afetam a tabela inteira.** Confirmar sempre o `WHERE`.
- **No Oracle as alterações só ficam definitivas com `COMMIT`.**

## SELECT: consultar

```sql
SELECT tec.nome AS tecnico, sl.nome AS servico
FROM   tecnico tec
JOIN   servico_local sl ON sl.codigo = tec.cod_servico   -- FK = PK
WHERE  sl.distrito = 'Leiria'
ORDER  BY tec.nome;
```

| Tipo de JOIN | Devolve |
|---|---|
| `INNER JOIN` (ou `JOIN`) | Só as linhas com correspondência nos dois lados |
| `LEFT JOIN` | Todas as da esquerda; `NULL` onde não há correspondência |
| `FULL OUTER JOIN` | Tudo dos dois lados |

**Agregação** (`WHERE` filtra linhas antes de agrupar; `HAVING` filtra grupos depois):

```sql
SELECT estado, COUNT(*) AS total
FROM   pedido
GROUP  BY estado
HAVING COUNT(*) > 10
ORDER  BY total DESC;
```

**Procurar violações de uma regra** (deferidos sem pagamento):

```sql
SELECT p.n_pedido
FROM   pedido p
LEFT   JOIN pagamento pg ON pg.n_pedido = p.n_pedido
WHERE  p.estado = 'Deferido'
AND    pg.id_pagamento IS NULL;
```

## Particularidades do Oracle

| Tema | Oracle |
|---|---|
| Alias de **tabela** | Sem `AS`: `FROM tecnico tec` (com `AS` dá erro) |
| Alias de **coluna** | Com `AS` (opcional): `nome AS tecnico` |
| Limitar linhas | `FETCH FIRST 5 ROWS ONLY` (12c ou superior); antes: `WHERE ROWNUM <= 5` |
| Consulta sem tabela | `SELECT SYSDATE FROM dual;` (`dual` é uma tabela de uma linha) |
| Data e hora atuais | `SYSDATE` |
| Valor por defeito se nulo | `NVL(coluna, 0)` ou `COALESCE(a, b, c)` |
| Comparar com nulo | `IS NULL` / `IS NOT NULL` (nunca `= NULL`) |
| Texto vazio | `''` é tratado como `NULL` no Oracle |
| Formatar datas | `TO_CHAR(data, 'DD/MM/YYYY')` |
| Nomes de objetos | Guardados em maiúsculas, salvo se criados entre aspas duplas |
| Concatenar texto | `\|\|` (ex.: `nome \|\| ' - ' \|\| distrito`) |

## Convenção de nomes das restrições

`pk_tabela`, `fk_tabela_referenciada`, `uk_tabela_coluna`, `ck_tabela_regra`.
