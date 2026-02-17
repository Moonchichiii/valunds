# Valund

High-trust competence marketplace for the Nordic region.

## Bootstrap commands

```bash
git checkout -b infra/bootstrap
uv sync --group dev
bun install
python manage.py makemigrations core
python manage.py migrate
pre-commit install
ruff check .
ruff format .
mypy .
```
