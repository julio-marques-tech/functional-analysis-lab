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