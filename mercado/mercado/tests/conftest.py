import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from vendas.models import Produtos, Carrinho

import inspect


test_reports = []


@pytest.fixture
def user(db):
    """Usuário autenticado padrão."""
    return User.objects.create_user(username="testuser",
                                    email="teste@exemplo.com",
                                    password="senha123")


@pytest.fixture
def produto(db, user):
    """Produto em estoque ligado ao usuário."""
    return Produtos.objects.create(
        nome="Produto A",
        descricao="Descrição do produto A",
        preco=100,
        quantidade_estoque=20,
        user=user
    )


@pytest.fixture
def carrinho(db, user, produto):
    """Item no carrinho (2 unidades)."""
    return Carrinho.objects.create(cliente=user,
                                   produto=produto,
                                   quantidade=2)


@pytest.fixture
def api_client(user):
    """APIClient já autenticado."""
    client = APIClient()
    client.login(username="testuser", password="senha123")
    return client


import pytest
import logging
import io
import inspect

# Acumula relatórios
test_reports = []

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    # Cria buffer e handler de logs para cada teste
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setLevel(logging.INFO)
    item._log_handler = handler
    item._log_buffer = buf
    logging.getLogger().addHandler(handler)

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    # Remove handler após teste
    logging.getLogger().removeHandler(item._log_handler)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Executa o relatório padrão
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    # Nome e status
    name = report.nodeid
    status = "PASSED" if report.passed else "FAILED"

    # Extrai docstring
    doc = item.obj.__doc__ or ""
    lines = inspect.cleandoc(doc).splitlines()
    identifier = lines[0] if lines else ""
    description = " ".join(lines[1:]).strip() if len(lines) > 1 else ""

    # Captura logs
    logs = item._log_buffer.getvalue().strip()

    # Captura propriedades definidas pelo teste (Entrada, Resultado is_valid, Erros…)
    props = {k: v for k, v in getattr(report, "user_properties", [])}

    # Mensagem de exceção, se houver
    error_msg = str(call.excinfo.value) if call.excinfo else ""

    test_reports.append({
        "name": name,
        "identifier": identifier,
        "description": description,
        "status": status,
        "input": props.get("Entrada"),
        "result_valid": props.get("Resultado is_valid"),
        "errors": props.get("Erros username") or props.get("Erros gerais"),
        "logs": logs,
        "error": error_msg
    })

def pytest_sessionfinish(session, exitstatus):
    # Gera o TXT no fim da sessão
    with open("resultado_testes.txt", "w", encoding="utf-8") as f:
        f.write("Relatório de Testes Pytest Detalhado\n")
        f.write("===================================\n\n")
        for rpt in test_reports:
            f.write(f"Teste: {rpt['name']}\n")
            if rpt['identifier']:
                f.write(f"Identificador: {rpt['identifier']}\n")
            if rpt['description']:
                f.write(f"Descrição: {rpt['description']}\n")
            if rpt['input'] is not None:
                f.write(f"Entrada: {rpt['input']}\n")
            if rpt['result_valid'] is not None:
                f.write(f"Resultado is_valid: {rpt['result_valid']}\n")
            if rpt['errors'] is not None:
                f.write(f"Erros capturados: {rpt['errors']}\n")
            if rpt['logs']:
                f.write("Logs:\n")
                f.write(rpt['logs'] + "\n")
            if rpt['status'] == "FAILED" and rpt['error']:
                f.write(f"Erro de execução: {rpt['error']}\n")
            f.write(f"Status: {rpt['status']}\n\n")
        f.write(f"Exit status pytest: {exitstatus}\n")