// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Mocking matchMedia for testing purposes
// This is necessary for components that use media queries or responsive design
// as matchMedia is not available in the Jest environment by default.
// This mock implementation returns a default state where no media queries match.
// You can customize the mock to return different states based on your tests.
// This is particularly useful for testing components that rely on dark mode or responsive styles.
// For example, if you want to test dark mode styles, you can modify the mock to
// return `matches: true` for the dark mode media query.
// This mock is compatible with Jest and can be used in your test setup file (e.g. setupTests.js).
// It allows you to simulate different media query states without needing a real browser
// environment, making your tests more predictable and easier to run in a CI/CD pipeline.
// src/setupTests.js
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(), // deprecated
        removeListener: jest.fn(), // deprecated
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
    })),
});

// Also mock localStorage for testing
Object.defineProperty(window, 'localStorage', {
    writable: true,
    value: {
        getItem: jest.fn(() => null),
        setItem: jest.fn(),
        removeItem: jest.fn(),
        clear: jest.fn(),
    },
});
