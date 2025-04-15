describe('Todo App', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000')
  })

  it('displays the Kanban board with correct columns', () => {
    cy.get('.kanban-column').should('have.length', 4)
    cy.contains('.column-header', 'Backlog')
    cy.contains('.column-header', 'In Progress')
    cy.contains('.column-header', 'In Review')
    cy.contains('.column-header', 'Done')
  })

  it('shows task counts in column headers', () => {
    cy.get('.column-header').each(($header) => {
      cy.wrap($header).find('.task-count').should('exist')
    })
  })

  it('allows adding a new task', () => {
    cy.get('[data-bs-target="#addTaskModal"]').click()
    cy.get('#id_title').type('Test Task')
    cy.get('form').submit()
    
    cy.contains('.task-item', 'Test Task').should('exist')
  })

  it('allows editing a task', () => {
    cy.get('.task-item').first().find('.btn-outline-primary').click()
    cy.get('#id_title').clear().type('Updated Task')
    cy.get('form').submit()
    
    cy.contains('.task-item', 'Updated Task').should('exist')
  })

  it('allows changing task status via drag and drop', () => {
    const dataTransfer = new DataTransfer()
    
    cy.get('.task-item').first()
      .trigger('dragstart', { dataTransfer })
    
    cy.get('.kanban-column[data-status="in_progress"] .column-drop-zone')
      .trigger('dragover', { dataTransfer })
      .trigger('drop', { dataTransfer })
    
    cy.get('.kanban-column[data-status="in_progress"]')
      .find('.task-item')
      .should('exist')
  })
}) 