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
