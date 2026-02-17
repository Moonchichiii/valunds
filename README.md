# Valund

High-trust Nordic competence marketplace bootstrap.

## Enterprise foundation

- Atomic domain architecture under `apps/`.
- Modular orchestration under `config/`.
- Tailwind CSS v4 zero-config entrypoint at `static/css/index.css`.
- HTMX + DRF unified selector pattern for reusable data flows.
## Atomic repository architecture

- `apps/` contains self-contained domain apps (`accounts`, `core`, `passports`, `bookings`).
- `config/` contains orchestration (`settings/`, `urls.py`, `asgi.py`, `wsgi.py`).
- `templates/layouts/` contains global shells (base/dashboard pages).
- Each app keeps HTMX components under `apps/<app>/templates/<app>/components/`.

## Initialization commands

```bash
# Python workspace (uv)
uv venv
uv sync --all-extras

# Frontend workspace (bun)
bun install
bun run watch:css

# Developer guardrails
uv run pre-commit install
uv run python manage.py check --settings=config.settings.local
uv run ruff check . --fix
uv run mypy apps
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
