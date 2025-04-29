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
from PIL import Image



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

def save(self, *args, **kwargs):
    if self.imagem:
        img = Image.open(self.imagem)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.imagem.path)
    super().save(*args, **kwargs)



# Página inicial com todos os produtos
@login_required
def index(request):
    try:
        produtos = Produtos.objects.all()
        return render(request, 'index.html', {'produtos': produtos})
    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao carregar os produtos: {str(e)}'}, status=500)

# Página de produtos do usuário
@login_required
def produtos_usuario(request):
    try:
        produtos = Produtos.objects.filter(user=request.user)
        return render(request, 'produtos_usuario.html', {'produtos': produtos})
    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao carregar seus produtos: {str(e)}'}, status=500)

# Adicionar um novo produto
@login_required
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            nome_produto = form.cleaned_data['nome']
            if Produtos.objects.filter(user=request.user, nome=nome_produto).exists():
                form.add_error('nome', 'Você já possui um produto com esse nome.')
                return render(request, 'adicionar_produto.html', {'form': form})

            produto = form.save(commit=False)
            produto.user = request.user  # Associa o produto ao usuário
            produto.save()
            return JsonResponse({'message': 'Produto adicionado com sucesso!'}, status=201)  # Feedback de sucesso
        else:
            return JsonResponse({'error': 'Dados inválidos no formulário'}, status=400)
    else:
        form = ProdutoForm()
    return render(request, 'adicionar_produto.html', {'form': form})

# Editar um produto existente
@login_required
def editar_produto(request, id):
    try:
        produto = get_object_or_404(Produtos, id=id)
        if request.method == 'POST':
            form = ProdutoForm(request.POST, request.FILES, instance=produto)
            if form.is_valid():
                form.save()
                # Resposta JSON com a mensagem de sucesso
                return JsonResponse({'message': 'Produto atualizado com sucesso!'}, status=200)
            else:
                return JsonResponse({'error': 'Erro ao atualizar o produto.'}, status=400)
        else:
            form = ProdutoForm(instance=produto)
        return render(request, 'editar_produto.html', {'form': form, 'produto': produto})
    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao editar o produto: {str(e)}'}, status=500)


# Excluir um produto
@login_required
def excluir_produto(request, id):
    try:
        produto = get_object_or_404(Produtos, id=id)
        produto.delete()
        return JsonResponse({'message': 'Produto excluído com sucesso!'}, status=200)  # Feedback de sucesso
    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao excluir o produto: {str(e)}'}, status=500)


# Adicionar ao carrinho
@login_required
def adicionar_ao_carrinho(request, id):
    try:
        produto = get_object_or_404(Produtos, id=id)
        carrinho_item, created = Carrinho.objects.get_or_create(cliente=request.user, produto=produto)
        if not created:
            carrinho_item.quantidade += 1
            carrinho_item.save()

        return JsonResponse({'message': 'Produto adicionado ao carrinho.'})  # Feedback de sucesso
    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao adicionar o produto ao carrinho: {str(e)}'}, status=500)
    

@login_required
def remover_do_carrinho(request, item_id):
    try:
        item = get_object_or_404(Carrinho, id=item_id, cliente=request.user)
        item.delete()
        return JsonResponse({'message': 'Produto removido do carrinho.'}, status=200)  # Sucesso com código 200
    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao remover o produto do carrinho: {str(e)}'}, status=500)
    
# Exibir carrinho
@login_required
def carrinho(request):
    try:
        carrinho = Carrinho.objects.filter(cliente=request.user)
        total = sum(item.total() for item in carrinho)
        return render(request, 'carrinho.html', {'cart_items': carrinho, 'total': total})
    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao carregar o carrinho: {str(e)}'}, status=500)

@login_required
def finalizar_compra(request):
    if request.method == "POST":
        itens = Carrinho.objects.filter(cliente=request.user)
        if not itens.exists():
            return JsonResponse({"error": "Carrinho vazio"}, status=400)

        total = sum(i.total() for i in itens)
        Vendas.objects.create(cliente=request.user, total=total)   # ⇐ mudou

        itens.delete()  # limpa carrinho
        return JsonResponse({"message": "Compra finalizada com sucesso"}, status=200)

    return JsonResponse({"error": "Método não permitido"}, status=405)



# Página de cadastro
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not email or not password or not password2:
            return JsonResponse({"error": "Todos os campos são obrigatórios."}, status=400)

        if password != password2:
            return JsonResponse({"error": "As senhas não coincidem."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Nome de usuário já está em uso."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "E-mail já está cadastrado."}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({"message": "Usuário cadastrado com sucesso!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro ao cadastrar o usuário: {str(e)}"}, status=500)
    
    return render(request, 'register.html')

# Página de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'Todos os campos são obrigatórios.'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas. Verifique seu nome de usuário ou senha.'})

    return render(request, 'login.html')
