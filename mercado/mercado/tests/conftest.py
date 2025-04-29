import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from vendas.models import Produtos, Carrinho


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
