# cybermag

# ✅ Local Validation Guide (Before You Push or Merge)

This document is a quick step-by-step checklist for **every developer** working on this project.

> 📌 You **must** follow this guide **before committing or pushing code** to `dev` or `main`.

---

## 🔁 Step-by-Step Development & Validation Flow

```
Developer (You)
  |
  └──> Start your feature branch from `dev`
        |
        └──> Code changes (frontend/backend or both)
              |
              └──> Run tests & linters (see below)
                    |
                    ├──> ✅ All local checks pass
                    |       └──> Commit and push your changes
                    |
                    └──> ❌ Tests fail / linter errors
                            └──> Fix and re-run
```

---

## 🧪 1. Test Your Backend Code (Flask)

📂 In `backend/`, make sure to:

### ✅ Run unit tests with coverage

```bash
cd backend
pytest --cov=. --cov-report=term-missing
```

- ✅ Required: No test failures
- ✅ Aim: ≥85% coverage for new features

🧠 Add tests in `backend/tests/` using `pytest`. Fixtures are auto-loaded from `conftest.py`.

### Example test:

```python
# backend/tests/test_example.py
def test_addition():
    assert 1 + 1 == 2
```

### 📚 Resources:
- Pytest: https://docs.pytest.org/en/stable/
- Flask Testing: https://flask.palletsprojects.com/en/latest/testing/
- Pytest-Cov: https://pytest-cov.readthedocs.io/

---

## 🌐 2. Test Your Frontend Code (React)

📂 In `frontend/`, make sure to:

### ✅ Run unit tests and coverage

```bash
cd frontend
npm test -- --coverage
```

- ✅ Required: No failing tests
- ✅ Coverage goal: ≥80%

💡 Tests live in `frontend/src/__tests__`

### Example test:

```jsx
// src/__tests__/App.test.js
import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders loading message', () => {
  render(<App />);
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
});
```

### 📚 Resources:
- React Testing Library: https://testing-library.com/docs/react-testing-library/intro
- Jest: https://jestjs.io/docs/getting-started

---

## 🧹 3. Run Linters (Auto Format)

### 🔧 Fix and check code automatically before commit:

```bash
make fix   # Auto-format with Black, Ruff
make lint  # Run flake8 and pylint
make test  # Run all Python tests
make check # Run all of the above
```

Or manually:

```bash
# Python
cd backend
flake8 .
pylint $(find . -name "*.py" | head -10)
black . --check
ruff check .

# JavaScript
cd frontend
npm run lint
```

### 📚 Linters:
- Black: https://black.readthedocs.io/
- Ruff: https://docs.astral.sh/ruff/
- Pylint: https://pylint.pycqa.org/
- ESLint: https://eslint.org/

---

## 🔒 4. Run Security Scan (Optional)

```bash
trivy fs .
```

(Or wait for GitHub Actions security check)

📚 https://aquasecurity.github.io/trivy

---

## ✅ Final Checklist

- [ ] Backend tests passed (`pytest`)
- [ ] Frontend tests passed (`npm test`)
- [ ] Lint checks passed (`make check`)
- [ ] I added tests for new features or fixed logic
- [ ] I did **not** push broken code

---

# Feature: UI Report Cards Grid

  ## 🚀 Objective
  Implement a modern, responsive design for report cards using Tailwind CSS in React. This includes visual integration with risk, summary, analysis, and adaptive grid mode.

  ## ✅ Main Changes

  - Installation and configuration of **Tailwind CSS v3**
  - Integration of the `@tailwindcss/line-clamp` plugin
  - `ReportCard.jsx` component:
  - Clickable title with icon
  - Summary and analysis (if available)
  - Risk level with dynamic color
  - “Show more” dropdown button
  - Responsive, modern, and clean style

  - Layout:
  - Used `grid-cols` to display multiple cards in rows and columns based on screen size.

## 🔧 Added Dependencies

```bash
  npm install -D tailwindcss postcss autoprefixer
  npm install -D @tailwindcss/line-clamp

## 💬 Questions?

Ask in the PR or review team channel (this channel is not yet implemented. Let’s keep this repo clean, tested, and ready for deployment 🙌
