const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8000',
    viewportWidth: 1280,
    viewportHeight: 800,
    defaultCommandTimeout: 10000,
    watchForFileChanges: true,
    video: false,
    screenshotOnRunFailure: true,
    trashAssetsBeforeRuns: true,
    excludeSpecPattern: ['**/node_modules/**'],
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
}) 