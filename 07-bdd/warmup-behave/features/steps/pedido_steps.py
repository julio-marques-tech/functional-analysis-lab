from behave import given, when, then


# Sistema simulado. Num projeto real, estes passos chamariam a UI (Playwright) ou a API.
def submeter_pedido(dependentes_elegiveis):
    if dependentes_elegiveis > 0:
        return {"registado": True, "estado": "Em análise", "mensagem": None}
    return {"registado": False, "estado": None, "mensagem": "Não existem dependentes elegíveis"}


@given('que o cidadão está autenticado no portal')
def step_autenticado(context):
    context.autenticado = True


@given('que o cidadão tem um dependente elegível a cargo')
def step_com_dependente(context):
    context.dependentes_elegiveis = 1


@given('que o cidadão não tem dependentes a cargo')
def step_sem_dependentes(context):
    context.dependentes_elegiveis = 0


@when('submete um novo pedido de abono de família')
def step_submete(context):
    assert context.autenticado, "O cidadão tem de estar autenticado"
    context.resultado = submeter_pedido(context.dependentes_elegiveis)


@then('o pedido fica registado com o estado "{estado}"')
def step_estado(context, estado):
    assert context.resultado["registado"], "O pedido devia estar registado"
    obtido = context.resultado["estado"]
    assert obtido == estado, f'Estado esperado "{estado}", obtido "{obtido}"'


@then('o pedido não é registado')
def step_nao_registado(context):
    assert not context.resultado["registado"], "O pedido não devia estar registado"


@then('é informado de que não existem dependentes elegíveis')
def step_informado(context):
    assert context.resultado["mensagem"] == "Não existem dependentes elegíveis"