import pytest
from django.urls import reverse
from vendas.models import Carrinho


def _msg(resp):
    """Funciona tanto para DRF Response quanto JsonResponse."""
    try:
        return resp.data["message"]
    except AttributeError:
        return resp.json().get("message", "")


# ---------- CT‑002  adicionar ----------
@pytest.mark.django_db
def test_api_adicionar_ao_carrinho(api_client, produto):
    resp = api_client.post(reverse("adicionar_ao_carrinho", args=[produto.id]))

    assert resp.status_code == 200
    assert Carrinho.objects.filter(produto=produto).exists()
    assert "adicionado" in _msg(resp).lower()


# ---------- CT‑003  remover ----------
@pytest.mark.django_db
def test_api_remover_do_carrinho(api_client, carrinho):
    resp = api_client.delete(reverse("remover_do_carrinho", args=[carrinho.id]))

    assert resp.status_code == 200
    assert not Carrinho.objects.filter(id=carrinho.id).exists()
    assert "removido" in _msg(resp).lower()


# ---------- CT‑004  finalizar ----------
@pytest.mark.django_db
def test_api_finalizar_compra(api_client, user, produto):
    Carrinho.objects.bulk_create([
        Carrinho(cliente=user, produto=produto, quantidade=1),
        Carrinho(cliente=user, produto=produto, quantidade=2),
    ])

    resp = api_client.post(reverse("finalizar_compra"))

    assert resp.status_code == 200
    assert "sucesso" in _msg(resp).lower()
    assert Carrinho.objects.filter(cliente=user).count() == 0
