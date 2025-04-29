import pytest
from django.urls import reverse
from django.test import Client
from vendas.models import Carrinho, Produtos


# ---------- CT‑001  cadastro + login ----------
@pytest.mark.django_db
def test_e2e_cadastro_login():
    client = Client()

    # cadastro (aceita 201 JSON ou 302 redirect)
    resp = client.post(reverse("register"), {
        "username": "novo",
        "email": "novo@exemplo.com",
        "password": "senha123",
        "password2": "senha123",
    })
    assert resp.status_code in (201, 302)

    # login (aceita 200 ou 302)
    resp = client.post(reverse("login"), {
        "username": "novo",
        "password": "senha123",
    })
    assert resp.status_code in (200, 302)


# ---------- CT‑002,003,004 encadeados ----------
@pytest.mark.django_db
def test_e2e_fluxo_compra(user, produto):
    client = Client()
    client.login(username="testuser", password="senha123")

    # adicionar
    client.post(reverse("adicionar_ao_carrinho", args=[produto.id]))
    assert Carrinho.objects.count() == 1

    # remover
    item = Carrinho.objects.first()
    client.delete(reverse("remover_do_carrinho", args=[item.id]))
    assert Carrinho.objects.count() == 0

    # adicionar dois produtos
    produto_b = Produtos.objects.create(
        nome="Produto B", descricao="desc", preco=50,
        quantidade_estoque=5, user=user
    )
    client.post(reverse("adicionar_ao_carrinho", args=[produto.id]))
    client.post(reverse("adicionar_ao_carrinho", args=[produto_b.id]))

    # finalizar
    resp = client.post(reverse("finalizar_compra"))
    assert resp.status_code == 200
    assert "sucesso" in resp.content.decode().lower()
