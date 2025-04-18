// scripts.js

// Função para confirmar a exclusão do produto no modal
document.querySelectorAll('.btn-danger').forEach(button => {
    button.addEventListener('click', function(event) {
        const confirmation = confirm("Tem certeza de que deseja excluir este produto?");
        if (!confirmation) {
            event.preventDefault();  // Cancela a ação de excluir
        }
    });
});


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
// Modal de confirmação de exclusão do produto
document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
    button.addEventListener('click', function(event) {
        const produtoId = button.dataset.produtoId;
        const modal = document.getElementById('produtoModal' + produtoId);

        modal.querySelector('.btn-danger').addEventListener('click', function() {
            fetch(`/produtos/excluir/${produtoId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Exibe um aviso de sucesso sem recarregar a página
                    alert(data.message);
                    modal.querySelector('.modal-close').click();  // Fecha o modal de confirmação
                    // Aqui você pode remover o produto da lista de produtos diretamente sem recarregar a página
                    const produtoElement = document.getElementById(`produto-${produtoId}`);
                    produtoElement.remove();  // Remove o produto da lista
                } else {
                    alert('Erro ao excluir o produto.');
                }
            })
            .catch(error => {
                console.error('Erro ao excluir o produto:', error);
                alert('Ocorreu um erro ao excluir o produto.');
            });
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


document.getElementById('adicionarCarrinhoForm')?.addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o comportamento padrão de envio do formulário

    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Exibe a mensagem de sucesso
            // Aqui você pode atualizar o conteúdo da página, como o contador do carrinho
        }
    })
    .catch(error => {
        console.error('Erro ao adicionar ao carrinho:', error);
    });
});
