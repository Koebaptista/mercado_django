// CT-010: Login de Usuário
describe('CT-010: Login de Usuário', () => {
  it('autentica usuário válido e redireciona para a página inicial', () => {
    // 1. Acessar a página de login
    cy.visit('/login') 

    // 2. Preencher nome de usuário e senha
    cy.get('input[name="username"]').type('batista')
    cy.get('input[name="password"]').type('AAAsdasd123@')

    // 3. Submeter o formulário
    cy.get('button[type="submit"]').click()

    // 4. Verificar redirecionamento para a home
    cy.url().should('eq', `${Cypress.config().baseUrl}/`)
  
  })

})

