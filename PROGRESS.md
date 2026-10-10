# Progress

Registo de cada módulo: o que foi feito, decisões técnicas, problemas encontrados e como
foram resolvidos.

## 07 · BDD: warm-up com behave

**Estado:** concluído (2026-09-30). Migrado do repositório `ai-automation-labs`.

Primeira feature file executável: Gherkin em português, step definitions com parâmetro e
passos reutilizados, ciclo verde/vermelho e execução filtrada por tags. Detalhes em
[07-bdd/warmup-behave/README.md](07-bdd/warmup-behave/README.md).

## 01 · Modelação de dados

**Estado:** concluído (2026-10-01 a 2026-10-08).

**Feito:**
- [DER conceptual](01-data-modeling/der-conceptual.md) completo, extraído da entrevista com
  a stakeholder: 19 entidades, catálogos, históricos com vigência, N:M resolvidos com
  entidades associativas, relacionamento recursivo N:M (dependentes)
- [Normalização](01-data-modeling/normalizacao.md) da folha de cálculo atual, da 1FN à FNBC,
  com dependências funcionais testadas nos dados, e critérios de desnormalização

**Decisões:**
- Notação Crow's Foot em Mermaid em vez de PlantUML: texto versionável que o GitHub desenha
  sem instalar nada
- Chave substituta (`id_cidadao`) + NISS único, em vez do NISS como chave primária

**Dificuldades e como foram resolvidas:**
- Ler a cardinalidade num só sentido, ou pôr "um" nas duas pontas: resolvido com o método
  das duas perguntas a partir de uma instância e a regra "o símbolo encostado a uma entidade
  conta essa entidade"
- Misturar requisitos funcionais (ecrãs, workflow) com dados: resolvido com as três lentes
  (dados / comportamento / regras)
- Confundir relacionamento recursivo com N:M: são dimensões independentes (tabela 2×2 no DER)
- Dependências funcionais por intuição: resolvido testando nos dados e procurando
  contraexemplos

## 02 · Arquitetura de dados

**Estado:** concluído, primeira passagem (2026-10-09 a 2026-10-10).

**Feito:** [resumo do módulo](02-data-architecture/arquitetura-de-dados.md): OLTP vs OLAP,
ODS / data warehouse / data mart, modelo em estrela (factos, dimensões, granularidade, DIM_TEMPO),
floco de neve, SCD tipos 1 a 3, Inmon vs Kimball, ETL vs ELT, data lake e lakehouse (camadas
bronze, silver, gold).

**Dificuldades e como foram resolvidas:**
- Cardinalidade na estrela: o "centro" do desenho não decide quem é o lado "muitos"; é a fact,
  que tem uma linha por evento. Regra: `||` na dimensão, `o{` na fact
- SCD2: a dimensão cresce ao ritmo das mudanças, não das transações (exercício com 3 linhas na
  dimensão e 262 na fact)
- Colunas de auditoria do transacional não pertencem a uma DIM_TEMPO, que é um calendário
- ETL vs ELT decide-se por onde corre a transformação, não pela ferramenta

