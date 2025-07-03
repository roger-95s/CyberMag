// jest.config.js
module.exports = {
    collectCoverage: true,
    collectCoverageFrom: [
        "src/**/*.{js,jsx,ts,tsx}",
        "!src/**/*.test.{js,jsx,ts,tsx}",
        "!src/index.js",
        "!src/reportWebVitals.js"
    ],
    coverageReporters: ["text", "lcov"],
    testEnvironment: "jsdom"
};
