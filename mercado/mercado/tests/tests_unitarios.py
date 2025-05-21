# arquivo testes_unitarios

import pytest
from django.contrib.auth.models import User
from vendas.forms import CustomUserCreationForm, ProdutoForm

import pytest
import logging
from vendas.forms import CustomUserCreationForm, ProdutoForm

logger = logging.getLogger(__name__)

import pytest
import logging
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from vendas.models import Produtos



@pytest.mark.django_db
def test_adicionar_produto_view_cria_produto(client, user, request):
    """
    CT-008: Cadastro de Produto (Sucesso)
    Validar a criação de um novo produto.
    """
    # 1) Login do usuário
    client.force_login(user)

    # 2) Dados de entrada
    image = SimpleUploadedFile(
        name="produto.jpg",
        content=b"fake-image-bytes",
        content_type="image/jpeg"
    )
    data = {
        'nome': 'Produto X',
        'descricao': 'Descrição do produto X',
        'preco': '100',                
        'quantidade_estoque': '5',     
    }
    files = {'imagem': image}

    # registra no relatório
    request.node.user_properties.append(("Entrada", {**data, 'imagem': 'produto.jpg'}))
    logger.info("Entrada adicionar_produto: %s + imagem produto.jpg", data)

    # 3) Chama a view
    url = reverse('adicionar_produto') 
    response = client.post(url, data, files=files)

    # log da resposta
    logger.info("Resposta adicionar_produto status=%s, content=%s", response.status_code, response.content)
    request.node.user_properties.append(("Status code", response.status_code))

    # 4) Asserções
    assert response.status_code == 201
    assert Produtos.objects.filter(nome='Produto X', user=user).exists()


@pytest.mark.django_db
def test_excluir_produto_view_remove_produto(client, user, produto, request):
    """
    CT-011: Excluir Produto (Sucesso)
    Validar a exclusão de um produto existente.
    """
    # 1) Login
    client.force_login(user)

    # 2) ID do produto a excluir
    prod_id = produto.id
    request.node.user_properties.append(("Entrada id", prod_id))
    logger.info("Entrada excluir_produto: id=%s", prod_id)

    # 3) Chama a view
    url = reverse('excluir_produto', args=[prod_id]) 
    response = client.get(url)

    # log da resposta
    logger.info("Resposta excluir_produto status=%s, content=%s", response.status_code, response.content)
    request.node.user_properties.append(("Status code", response.status_code))

    # 4) Asserções
    assert response.status_code == 200
    assert not Produtos.objects.filter(id=prod_id).exists()

@pytest.mark.django_db
def test_custom_user_creation_form_duplicate_username(user, request):
    """
    CT-015: Cadastro de usuário duplicado (Erro)
    Deve rejeitar quando o username já existe no DB.
    """
    form_data = {
        'username': user.username,
        'email': 'novo_email@example.com',
        'password1': 'SenhaForte123',
        'password2': 'SenhaForte123'
    }

    # registra entrada nos user_properties
    request.node.user_properties.append(("Entrada", form_data))
    logger.info("Entrada: %s", form_data)

    form = CustomUserCreationForm(data=form_data)
    valid = form.is_valid()
    request.node.user_properties.append(("Resultado is_valid", valid))
    logger.info("Form.is_valid() -> %s", valid)

    assert not valid

    errors = form.errors.get('username', [])
    request.node.user_properties.append(("Erros username", errors))
    logger.info("Erros username: %s", errors)

    assert 'Este nome de usuário já está em uso.' in errors

@pytest.mark.django_db
def test_produto_form_missing_nome(request):
    """
    CT-016: Criação de Produto sem nome (Erro)
    Deve rejeitar quando o campo 'nome' estiver ausente.
    """
    data = {
        'descricao': 'Descrição teste',
        'preco': 50,
        'quantidade_estoque': 10
    }

    request.node.user_properties.append(("Entrada", data))
    logger.info("Entrada produto sem nome: %s", data)

    form = ProdutoForm(data=data)
    valid = form.is_valid()
    request.node.user_properties.append(("Resultado is_valid", valid))
    logger.info("Form.is_valid() -> %s", valid)

    errors = form.errors
    request.node.user_properties.append(("Erros gerais", errors))
    logger.info("Erros gerais: %s", errors)

    assert not valid
    assert 'nome' in errors