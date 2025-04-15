// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

Cypress.Commands.add('createTask', (title, description, status = 'open') => {
  cy.visit('/tasks/create/')
  cy.get('#id_title').type(title)
  cy.get('#id_description').type(description)
  cy.get('#id_status').select(status)
  cy.get('form').submit()
})

Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login/')
  cy.get('#id_username').type(username)
  cy.get('#id_password').type(password)
  cy.get('form').submit()
})

// Force click command for elements that might be covered
Cypress.Commands.add('forceClick', {prevSubject: 'element'}, (subject) => {
  cy.wrap(subject).click({force: true})
}) 