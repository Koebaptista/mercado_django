// scripts.js


document.getElementById('adicionarProdutoForm')?.addEventListener('submit', function(event) {
    event.preventDefault();  // Impede o envio normal do formulário

    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value  // Inclui o CSRF Token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Exibe a mensagem de sucesso
            window.location.href = '/produtos'; // Redireciona para a página de produtos do usuário
        } else {
            alert('Erro ao adicionar o produto.');
        }
    })
    .catch(error => {
        console.error('Erro ao adicionar produto:', error);
        alert('Ocorreu um erro inesperado.');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const errorMessage = document.querySelector('.alert-danger');
    if (errorMessage) {
        alert(errorMessage.textContent); // Exibe a mensagem de erro
    }
});


// Função para atualizar a quantidade de produtos no carrinho
document.querySelectorAll('.quantidade-input').forEach(input => {
    input.addEventListener('change', function(event) {
        const produtoId = input.dataset.produtoId;
        const novaQuantidade = input.value;

        fetch(`/atualizar_quantidade/${produtoId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            },
            body: JSON.stringify({ quantidade: novaQuantidade })
        })
        .then(response => response.json())
        .then(data => {
            if (data.sucesso) {
                alert('Quantidade atualizada com sucesso!');
                location.reload();  // Atualiza a página para refletir a mudança
            } else {
                alert('Erro ao atualizar a quantidade.');
            }
        });
    });
});

// Função para editar o produto (tratamento via AJAX)
document.querySelectorAll('.editarProdutoForm').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        const formData = new FormData(this);
        const produtoId = this.dataset.produtoId; // Assume que você tem um data-produto-id no formulário

        fetch(`/produtos/editar/${produtoId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message); // Exibe a mensagem de sucesso
                window.location.href = "/produtos"; // Redireciona para a página de produtos do usuário
            } else {
                alert('Erro ao editar o produto.');
            }
        })
        .catch(error => {
            console.error('Erro ao editar o produto:', error);
            alert('Ocorreu um erro ao tentar editar o produto.');
        });
    });
});



document.addEventListener('DOMContentLoaded', function() {
    // Modal de confirmação de exclusão do produto
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function(event) {
            const produtoId = button.dataset.produtoId;  // Obtém o ID do produto do botão
            console.log('Produto ID:', produtoId);  // Verifica se o ID está correto
            
            const confirmation = confirm("Tem certeza de que deseja excluir este produto do seu carrinho?");
            
            if (confirmation) {
                // Envia a requisição para excluir o produto do carrinho via AJAX
                fetch(`/carrinho/remover/${produtoId}/`, {  // Caminho correto da URL
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                    }
                })
                .then(response => response.json())  // Corrige a referência ao 'response'
                .then(data => {
                    if (data.message) {  // Verifica se a resposta foi bem-sucedida
                        alert(data.message);  // Exibe a mensagem de sucesso
                        // Remove o produto da lista diretamente sem recarregar a página
                        const produtoElement = document.getElementById(`produto-${produtoId}`);
                        if (produtoElement) {
                            produtoElement.remove();
                        }
                    } else {
                        alert(data.error || 'Erro desconhecido ao remover o produto.');
                    }
                })
                .catch(error => {
                    console.error('Erro ao excluir o produto:', error);
                    alert('Ocorreu um erro ao excluir o produto.');
                });
            }
        });
    });
});


// Função de login com o Google
const googleLoginButton = document.querySelector('.btn-google');
if (googleLoginButton) {
    googleLoginButton.addEventListener('click', function(event) {
        // Aqui você pode adicionar alguma lógica para realizar o login com o Google se necessário.
        // Atualmente, o formulário de login com Google já é tratado pela URL do Django.
    });
}

// Ações relacionadas ao formulário de cadastro de usuário
document.querySelector('#formCadastro')?.addEventListener('submit', function(event) {
    const senha = document.querySelector('#password').value;
    const senhaConfirmacao = document.querySelector('#password2').value;

    if (senha !== senhaConfirmacao) {
        event.preventDefault();  // Impede o envio do formulário
        alert("As senhas não coincidem!");
    }
});

// Ação para o carrinho de compras
document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('click', function(event) {
        // Essa ação pode ser expandida caso você deseje realizar validações antes de adicionar ao carrinho
        console.log('Produto adicionado ao carrinho');
    });
});

document.querySelectorAll('#adicionarCarrinhoForm').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Impede o envio normal do formulário

        const formData = new FormData(this);

        // Envia a requisição para o backend via AJAX
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value  // Inclui o CSRF Token
            }
        })
        .then(response => response.json())  // Espera resposta JSON
        .then(data => {
            if (data.message) {
                alert(data.message); // Exibe a mensagem de sucesso
                // Atualiza o contador ou a lista do carrinho conforme necessário
                console.log('Produto adicionado ao carrinho');
                // Caso precise redirecionar ou atualizar a UI, faça isso aqui
            } else {
                alert('Erro ao adicionar o produto ao carrinho.');
            }
        })
        .catch(error => {
            console.error('Erro ao adicionar ao carrinho:', error);
            alert('Ocorreu um erro inesperado.');
        });
    });
});
