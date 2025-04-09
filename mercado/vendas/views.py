from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Produtos
from .models import Clientes
from .forms import ProdutoForm
from .models import Produtos, Clientes, Vendas, Carrinho
from .serializers import ProdutosSerializer, ClientesSerializer, VendasSerializer, CarrinhoSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

@login_required
def produtos(request):
    produtos = Produtos.objects.all()
    return render(request, 'produtos.html', {'produtos': produtos})

def index(request):
    return render(request, 'index.html')


class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializer
    permission_classes = [IsAuthenticated]

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [IsAuthenticated]

class VendasViewSet(viewsets.ModelViewSet):
    queryset = Vendas.objects.all()
    serializer_class = VendasSerializer
    permission_classes = [IsAuthenticated]

class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer
    permission_classes = [IsAuthenticated]



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Verifique se as senhas são iguais
        if password != password2:
            return JsonResponse({"error": "As senhas não coincidem"}, status=400)
        
        # Crie um novo usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return JsonResponse({"message": "Usuário cadastrado com sucesso!"}, status=201)
    
    return render(request, 'register.html')  # Página de cadastro
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Verifica as credenciais do usuário
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')  # Obtém o próximo URL (se fornecido)
            return redirect(next_url)  # Redireciona para o URL original ou para a página inicial
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'login.html')