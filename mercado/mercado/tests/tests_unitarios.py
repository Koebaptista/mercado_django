# arquivo testes_unitarios

import pytest
from django.contrib.auth.models import User
from vendas.models import Produtos, Carrinho

# CT‑002 • cálculo do total
def test_total_basico(carrinho):
    assert carrinho.total() == 200   # 2 × 100


# variações de quantidade
@pytest.mark.parametrize("qtd,total", [(1, 100), (3, 300), (5, 500)])
def test_total_varios(qtd, total, user, produto):
    carrinho = Carrinho.objects.create(cliente=user,
                                       produto=produto,
                                       quantidade=qtd)
    assert carrinho.total() == total


# aumentar quantidade
def test_incrementa_quantidade(carrinho):
    carrinho.quantidade += 1
    carrinho.save()
    assert carrinho.quantidade == 3
    assert carrinho.total() == 300


# remover item
def test_remove_item(carrinho):
    carrinho_id = carrinho.id
    carrinho.delete()
    assert not Carrinho.objects.filter(id=carrinho_id).exists()