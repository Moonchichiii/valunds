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

## Testing strategy

- **Unit/Integration**: `pytest` for fast domain/service checks.
- **E2E**: Playwright-driven browser checks in `tests/e2e/` (set `E2E_BASE_URL`).
- **Static quality**: Ruff + Mypy in CI.
