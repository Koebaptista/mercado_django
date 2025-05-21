// cypress/e2e/CT-012-cadastro-incompativel.spec.cy.js

describe('CT-012: Cadastro com Senha Incompatível (Erro)', () => {
  const username = 'usuario_teste';
  const email = 'usuario_teste@example.com';
  const senha = 'SenhaForte123';
  const senhaDiferente = 'SenhaDiferente456';

  it('não cadastra usuário quando as senhas não coincidem e exibe erro apropriado', () => {
    // 1. Acessar a página de cadastro
    cy.visit('/register');

    // 2. Preencher campo “Nome de usuário”
    cy.get('input[name="username"]').type(username);

    // 3. Preencher campo “Email”
    cy.get('input[name="email"]').type(email);

    // 4. Preencher “Senha” e “Confirmar Senha” com valores diferentes
    cy.get('input[name="password1"]').type(senha);
    cy.get('input[name="password2"]').type(senhaDiferente);

    // 5. Submeter o formulário
    cy.get('button[type="submit"]').click();

    // 6. Verificar que permanece na página de cadastro
    cy.url().should('include', '/register');

    // 7. Verificar mensagem de erro genérica no topo
    cy.contains('Por favor corrija os erros abaixo.').should('be.visible');

    // 8. Verificar erro específico abaixo do campo de confirmação
    cy.get('ul.errorlist')
      .should('contain.text', 'The two password fields didn’t match.');
  });
});
