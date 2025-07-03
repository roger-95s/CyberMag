# Run auto-fix tools
fix:
	black .
	ruff format .  # optional; black already handles formatting
	ruff check . --fix

# Run all linters
lint:
	flake8 .
	pylint $(find . -name "*.py")

# Run tests
test:
	pytest

# Run all checks
check: fix lint test
