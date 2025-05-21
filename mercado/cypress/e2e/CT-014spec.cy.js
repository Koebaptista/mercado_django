// cypress/e2e/CT-014-cadastro-sucesso.spec.cy.js

describe('CT-014: Cadastro de Usuário Válido (Sucesso)', () => {
  const timestamp = Date.now();
  const newUsername = `novo_usuario_${timestamp}`;
  const newEmail = `novo_usuario_${timestamp}@example.com`;
  const senha = 'SenhaForte123';

  it('cadastra usuário válido e redireciona para o login com mensagem de sucesso', () => {
    // 1. Acessar a página de cadastro
    cy.visit('/register');

    // 2. Preencher “Nome de usuário” com valor único
    cy.get('input[name="username"]').type(newUsername);

    // 3. Preencher “Email” com valor único
    cy.get('input[name="email"]').type(newEmail);

    // 4. Preencher “Senha” e “Confirmar Senha”
    cy.get('input[name="password1"]').type(senha);
    cy.get('input[name="password2"]').type(senha);

    // 5. Submeter o formulário
    cy.get('button[type="submit"]').click();

    // 6. Verificar redirecionamento para /login
    cy.url().should('include', '/login');

    // 7. Verificar exibição da mensagem de sucesso
    cy.contains('Cadastro realizado com sucesso! Faça login.').should('be.visible');
  });
});
