# Warm-up BDD: executar uma feature file real com `behave`

> Versão em português. A versão em inglês vem depois, para alinhar com o resto do repositório.

Mini-prática feita antes do Lab 00 da trilha de BDD, para sair da teoria e ver o ciclo
completo de uma feature file: **especificação em Gherkin → passos por definir → step
definitions → verde → vermelho → execução filtrada por tags**.

## Contexto

Na minha prática como analista funcional (SPMS), escrevo cenários Gherkin dentro das
especificações de casos de uso, com matriz de cobertura contra as regras de negócio. Esses
cenários funcionam como especificação e critério de aceitação, mas **nunca foram
executados**. A automação não estava no âmbito do projeto.

Este warm-up fecha esse gap de forma mínima: uma feature file escrita por mim, ligada a
código Python e executada de verdade.

**Limite honesto:** é uma prova de conceito com um **sistema simulado** (uma função Python
que imita a regra de negócio). Não é automação contra uma aplicação real. Essa parte vem nos
Labs 01 e 02 da trilha (`pytest-bdd` + Playwright).

## Estrutura

```
warmup-behave/
├── features/
│   ├── pedido_abono.feature      ← especificação em Gherkin (português)
│   └── steps/
│       └── pedido_steps.py       ← step definitions (glue code) + sistema simulado
├── requirements.txt
└── README.md
```

## Como correr

```powershell
cd 10-bdd-test-automation\warmup-behave
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m behave                        # todos os cenários
python -m behave --tags=@smoke          # só os cenários de smoke
python -m behave --tags="not @smoke"    # tudo exceto smoke
```

> Usa-se `python -m behave` e não `behave` diretamente. Ver o problema 2 em baixo.

## A feature

Domínio: pedido de abono de família (exemplo ilustrativo, sem regras reais da Segurança Social).

```gherkin
# language: pt
@UC-07 @abono
Funcionalidade: Pedido de abono de família
    Como cidadão com dependentes a cargo
    Quero pedir o abono de família online
    Para receber a prestação sem ir a um balcão

    Contexto:
        Dado que o cidadão está autenticado no portal

    @smoke
    Cenário: Pedido submetido fica registado para análise
        Dado que o cidadão tem um dependente elegível a cargo
        Quando submete um novo pedido de abono de família
        Então o pedido fica registado com o estado "Em análise"

    Cenário: Pedido recusado sem dependentes elegíveis
        Dado que o cidadão não tem dependentes a cargo
        Quando submete um novo pedido de abono de família
        Então o pedido não é registado
        E é informado de que não existem dependentes elegíveis
```

Decisões de escrita:

- **Estilo declarativo:** descreve *o quê* (submeter um pedido), não *o como* (cliques,
  menus, campos). Se o ecrã mudar, o cenário continua válido.
- **`Contexto`** (Background) para o login, que é comum aos dois cenários e não é o
  comportamento em teste.
- **Um comportamento por cenário:** caminho feliz e caminho negativo separados.
- **Um só `Quando` por cenário**, com uma ação de negócio.
- **`Então` só com resultados observáveis**, nunca com ações.
- **Tags** com dois papéis: rastreabilidade (`@UC-07`) e seleção de execução (`@smoke`).

## O que foi feito, passo a passo

### 1. Ambiente

`venv` próprio da pasta e `behave 1.3.3` instalado.

### 2. Feature escrita e primeira execução: passos *undefined*

Sem código ligado, o `behave` leu e interpretou o Gherkin (língua, tags, narrativa,
`Contexto`, cenários) e marcou os passos como **undefined**:

```
0 scenarios passed, 0 failed, 2 error, 0 skipped
0 steps passed, 0 failed, 0 skipped, 9 undefined
```

O que isto mostrou:

- O **`Contexto` corre antes de cada cenário** (aparece repetido nos dois), por isso são 9
  passos (4 + 5) e não 8.
- O `behave` sugeriu **7 esqueletos de código para 9 passos**, porque o passo do `Contexto`
  e o `Quando` repetido precisam de **uma só** definição cada. Isto é a reutilização de
  passos a funcionar.
- Os decoradores do código são sempre `@given/@when/@then`, mesmo com a feature em
  português. A língua só se aplica ao ficheiro `.feature`.
- Este estado "especificação sem automação" é exatamente o estado dos cenários na SPMS.

### 3. Step definitions: verde

Cada passo ficou ligado a uma função Python. Pontos-chave do
[`pedido_steps.py`](features/steps/pedido_steps.py):

- **Parâmetro:** `'o pedido fica registado com o estado "{estado}"'`. O texto entre aspas
  no Gherkin chega à função como variável. É o equivalente às Cucumber Expressions
  (`{string}`) do Cucumber-JVM.
- **`context`:** o objeto partilhado entre os passos do mesmo cenário. O `Dado` guarda o
  estado, o `Quando` usa-o e o `Então` verifica-o.
- **Asserções com mensagem de negócio**, para uma falha se perceber sem abrir o código.

```
1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
9 steps passed, 0 failed, 0 skipped
```

### 4. Vermelho provocado de propósito

Mudei o estado esperado na feature para `"Deferido"` sem mexer no código, simulando uma
regra alterada sem aviso ou uma especificação desatualizada:

```
ASSERT FAILED: Estado esperado "Deferido", obtido "Em análise"

Failing scenarios:
  features/pedido_abono.feature:12  Pedido submetido fica registado para análise

1 scenario passed, 1 failed, 0 skipped
8 steps passed, 1 failed, 0 skipped
```

O que isto mostrou:

- A falha aponta o **passo exato** e a **linha da feature**, com uma mensagem legível pelo negócio.
- O outro cenário **continua verde**: os cenários são independentes.
- **Um cenário vermelho não diz quem está errado.** Pode ser defeito no código ou
  especificação desatualizada. Decidir qual é trabalho do analista com o QA e o programador.
  É isto que faz das feature files "documentação viva".

### 5. Execução filtrada por tags

```
python -m behave --tags=@smoke
1 scenario passed, 0 failed, 1 skipped
4 steps passed, 0 failed, 5 skipped
```

O mesmo mecanismo serve para correr só a regressão (`@regressao`) ou excluir cenários que
ainda não podem correr (`not @bloqueado`, `not @manual`). A sintaxe é praticamente igual no
Cucumber.

## Problemas encontrados e como foram resolvidos

| # | Problema | Causa | Solução |
|---|---|---|---|
| 1 | `ConfigError: No steps directory in ...\features` | O `behave` exige a pasta `features/steps` mesmo antes de haver código | Criar `features\steps` antes da primeira execução |
| 2 | `Program 'behave.exe' failed to run: An Application Control policy has blocked this file` | O Windows (Smart App Control) bloqueia executáveis sem assinatura, como o atalho `behave.exe` que o `pip` cria no `venv` | Correr como módulo: `python -m behave`. O `python.exe` é assinado e permitido. **Não** se desativa a política de segurança |
| 3 | Passo que deixaria de ter correspondência (*undefined*) | O texto do passo tem de coincidir **exatamente** com o da step definition. Escrevi "é informado **que**" na feature, e a forma correta é "é informado **de que**" | Corrigido nos **dois** sítios (feature e código). Lição: a consistência da escrita do analista afeta diretamente quem automatiza |
| 4 | Linhas duplicadas na saída do terminal | O formatador do `behave` reescreve a linha com cor quando o passo termina, e o terminal do VS Code mostra as duas versões | Nenhuma. É apenas visual, não afeta o resultado |

## O que aprendi

- Feature file, step definition e sistema em teste são três camadas distintas. O analista é
  dono da primeira, mas a forma como a escreve define o custo das outras duas.
- Escrita declarativa e passos reutilizáveis reduzem código de automação e manutenção.
- Um cenário executável deixa de poder ficar desatualizado sem que alguém dê por isso.
- Tags ligam a especificação ao pipeline: rastreabilidade e seleção de execução no mesmo
  mecanismo.

## Próximos passos

- **Lab 00 da trilha:** feature file craft (refatorar e rever cenários, incluindo gerados por IA).
- **Lab 01:** a mesma abordagem com `pytest-bdd`.
- **Lab 02:** ligar os passos a uma UI real com Playwright, substituindo o sistema simulado.
