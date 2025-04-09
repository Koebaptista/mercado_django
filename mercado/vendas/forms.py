# vendas/forms.py

from django import forms
from .models import Produtos
from .models import Clientes

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = ['nome', 'descricao', 'preco', 'quantidade_estoque']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nome', 'email', 'telefone']