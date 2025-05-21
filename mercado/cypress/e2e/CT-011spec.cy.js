// CT-011: Login de Usuário com Credenciais Inválidas
describe('CT-011: Login de Usuário com Credenciais Inválidas', () => {
  it('não autentica usuário inválido e exibe mensagem de erro', () => {
    // 1. Acessar a página de login
    cy.visit('/login') 

    // 2. Preencher nome de usuário válido e senha inválida
    cy.get('input[name="username"]').type('batista')
    cy.get('input[name="password"]').type('senhaErrada')

    // 3. Submeter o formulário
    cy.get('button[type="submit"]').click()

    // 4. Verificar que permanece na página de login
    cy.url().should('include', '/login')

    // 5. Verificar exibição da mensagem de erro
    cy.contains('Nome de usuário ou senha incorretos').should('be.visible')
  })
})
