# Valund

High-trust Nordic competence marketplace bootstrap.

## Initialization commands

```bash
# Python workspace (uv)
uv venv
uv sync --all-extras

# Frontend workspace (bun)
bun install

# Developer guardrails
uv run pre-commit install
uv run python manage.py check --settings=config.settings.local
uv run ruff check .
uv run mypy .
```

## GitHub governance bootstrap (optional)

```bash
gh milestone create --title "M1: The Shield" --description "Base infra: uv, bun, ruff, mypy, and pre-commit hooks."
gh milestone create --title "M2: The Passport" --description "Core Auth, BankID logic, and PII scrubbing for AI safety."
gh milestone create --title "M3: The Market" --description "Sector modules (Health/Blue-collar) and Search/Discovery."
gh milestone create --title "M4: The Vault" --description "Stripe Connect, Escrow logic, and Net-Pay calculations."
```
