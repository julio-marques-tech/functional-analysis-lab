# Roadmap

Objetivo: dominar, ao nível de conversa técnica aprofundada, e com prova prática, os temas
centrais da análise funcional: modelação e arquitetura de dados, SQL/Oracle, engenharia de
requisitos, BDD, metodologias e controlo de versões. Tudo aplicado ao mesmo caso de estudo.

## Caso de estudo

**Sistema de Gestão de Prestações Sociais** (fictício): cidadãos submetem pedidos de
prestações (ex.: abono de família), técnicos analisam a elegibilidade, os pedidos deferidos
geram pagamentos. É simples o bastante para caber num portfólio e rico o bastante para ter
N:M, histórico, regras de negócio, estados e integrações.

## Módulos e ordem

A ordem segue o peso de cada tema numa entrevista técnica de análise funcional: primeiro o
que se conversa (modelação, arquitetura de dados, requisitos, raciocínio), depois a prática
de execução (Oracle, Cucumber, Playwright).

| Ordem | Módulo | Conteúdo | Entregável |
|---|---|---|---|
| 1 | **01 · Modelação de dados** | Modelos conceptual/lógico/físico; notações Chen e Crow's Foot; entidades, atributos, relacionamentos, cardinalidade e participação; chaves (natural, substituta, composta, candidata); N:M e entidades associativas; entidades fracas; generalização/especialização. Normalização 1FN → 3FN e FNBC, com anomalias. Desnormalização: quando, porquê, custos | Normalização de um dataset "plano" passo a passo; DER do caso a partir de uma entrevista simulada (PlantUML) |
| 2 | **02 · Arquitetura de dados** | OLTP vs OLAP; ODS; data warehouse (Inmon vs Kimball); data marts; esquema em estrela e floco de neve; factos, dimensões, granularidade; SCD 1/2/3; ETL vs ELT; data lake, lakehouse; qualidade de dados, linhagem, dados mestre | Modelo dimensional do caso; descrição de uma arquitetura EBS → ODI → ODS → BI |
| 3 | **03 · Engenharia de requisitos** | Técnicas de levantamento (BABOK); organização e templates; requisitos de dados (glossário, dicionário de dados, matriz CRUD, regras → restrições); especificação de casos de uso; user stories, INVEST, critérios de aceitação; requisitos não funcionais; rastreabilidade; UML (casos de uso, sequência, atividades, estados) e BPMN | Pacote de análise do caso: UC, histórias, dicionário de dados, diagramas |
| 4 | **04 · Playbook de análise** | Método para abordar um cenário: contexto e stakeholders → AS-IS → problema → TO-BE → requisitos → priorização → validação; perguntas a fazer; riscos | Playbook + casos resolvidos |
| 5 | **05 · Metodologias e controlo de versões** | Waterfall, modelo em V, Agile, Scrum, Kanban, híbridos; MoSCoW, WSJF, Kano, valor × esforço; estimação; Git (branch, merge, conflitos, PR) e SVN (checkout/update/commit, trunk/branches/tags, locking) | Backlog priorizado do caso; repositório SVN local com histórico |
| 6 | **06 · Oracle e SQL** | Instância vs base de dados, schema = utilizador, tablespaces, tipos de dados, sequences/identity, views e materialized views, índices B-tree e bitmap, PL/SQL (procedure, function, package, trigger), `EXPLAIN PLAN`; prática com Oracle Database Free em Docker: DDL do caso, consultas, validação | Scripts DDL/DML e consultas do caso |
| 7 | **07 · BDD** | Gherkin avançado (Outline, Data Tables, `Regra`, anti-padrões, matriz de cobertura); behave (warm-up feito); Cucumber-JVM; Playwright a ligar passos a uma UI real | Feature files do caso, executáveis |
| 8 | **08 · Simulações** | Casos com tempo, perguntas técnicas, revisão final | Registo das simulações e aprendizagens |

## Calendário da primeira passagem

| Dia | Foco |
|---|---|
| 1 a 8 out | 01 · Modelação de dados: DER conceptual e normalização (1FN–3FN) |
| Qui 8 out (noite) | 01 · FNBC e desnormalização |
| Sex 9 out | 02 · Arquitetura de dados |
| Sáb 10 out (dia inteiro) | 03 · Engenharia de requisitos + 04 · Playbook de análise (casos com tempo) |
| Dom 11 out (dia inteiro) | 05 · Metodologias e controlo de versões + 06 · Oracle e SQL + 07 · BDD (Cucumber, Playwright) + 08 · Simulação completa |
| Seg 12 out (manhã) | Revisão das respostas prontas |

A ordem é por prioridade: os módulos 01 a 04 primeiro. Se algum dia derrapar, a parte
prática de 06 e 07 é a que passa para depois.
