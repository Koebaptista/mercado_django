from django.contrib import admin
from .models import Produtos, Clientes, Vendas

admin.site.register(Produtos)
admin.site.register(Clientes)
admin.site.register(Vendas)
