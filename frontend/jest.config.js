// frontend/jest.config.js
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'], // if you have a setup file
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: { // Handle module aliases
    '^@/components/(.*)$': '<rootDir>/src/components/$1',
    '^@/types/(.*)$': '<rootDir>/src/types/$1',
    // Add other aliases here if needed, e.g., for '@/lib/(.*)$'
    '^@/lib/(.*)$': '<rootDir>/src/lib/$1',
  },
};

module.exports = createJestConfig(customJestConfig);
