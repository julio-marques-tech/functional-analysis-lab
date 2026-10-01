# functional-analysis-lab

Um portfólio prático de **análise funcional e de negócio**, construído à volta de um único
caso de estudo: um sistema fictício de gestão de prestações sociais. Cada módulo acrescenta
uma camada ao mesmo caso, como acontece num projeto real:

```
problema de negócio → análise → modelo conceptual → lógico → físico (Oracle)
→ SQL → casos de uso e user stories → feature files (Gherkin)
→ testes executáveis (behave, Cucumber, Playwright) → versionado em Git e SVN
```

> Os documentos de estudo estão em português nesta fase. A versão em inglês vem depois.

## Módulos

| # | Módulo | Estado |
|---|---|---|
| — | [Caso de estudo](case-study/) | Em curso |
| 01 | [Modelação de dados](01-data-modeling/): conceptual, lógico, físico, normalização, desnormalização | Em curso |
| 02 | [Arquitetura de dados](02-data-architecture/): OLTP/OLAP, ODS, data warehouse, data lake, ETL/ELT | Por começar |
| 03 | [Engenharia de requisitos](03-requirements-engineering/): levantamento, requisitos de dados, UC, user stories, UML/BPMN | Por começar |
| 04 | [Playbook de análise](04-analysis-playbook/): como abordar um problema ou cenário | Por começar |
| 05 | [Metodologias e controlo de versões](05-methodologies-version-control/): Waterfall, Agile, priorização, Git, SVN | Por começar |
| 06 | [Oracle e SQL](06-oracle-sql/): conceitos Oracle e prática com Oracle Database Free | Por começar |
| 07 | [BDD](07-bdd/): Gherkin, behave, Cucumber-JVM, Playwright | [Warm-up](07-bdd/warmup-behave/) feito |
| 08 | [Simulações](08-mock-interviews/): casos e perguntas técnicas com tempo | Por começar |

Plano detalhado em [ROADMAP.md](ROADMAP.md) e registo do progresso em [PROGRESS.md](PROGRESS.md).

## Sobre o autor

Analista funcional e de negócio com mais de 17 anos em TI: Oracle E-Business Suite, BI
(ODI/ODS/Qlik), e-commerce, retalho e saúde digital (FHIR/HL7). Este repositório consolida e
aprofunda essa prática num caso completo e público.
