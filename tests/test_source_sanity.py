"""Source-level guards for accidental merge artifact corruption."""

from __future__ import annotations

import ast
from pathlib import Path

CHECKS: dict[str, dict[str, int]] = {
    "apps/accounts/models.py": {"CustomUser": 1},
    "apps/passports/models.py": {"CompetencePassport": 1, "Credential": 1},
    "apps/passports/selectors.py": {"get_passport_context": 1},
    "apps/passports/services.py": {
        "credential_verify_tier3": 1,
        "credential_audit_expiry": 1,
    },
    "apps/passports/selectors.py": {"get_passport_data": 1},
    "apps/passports/services.py": {"credential_verify_tier3": 1},
}


def _count_defs(tree: ast.AST) -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            counts[node.name] = counts.get(node.name, 0) + 1
    return counts


def test_key_modules_parse_as_valid_python() -> None:
    files = list(CHECKS.keys()) + ["apps/passports/views.py", "config/asgi.py"]
    for file_path in files:
        source = Path(file_path).read_text(encoding="utf-8")
        ast.parse(source, filename=file_path)


def test_expected_definitions_are_not_duplicated() -> None:
    for file_path, expected in CHECKS.items():
        source = Path(file_path).read_text(encoding="utf-8")
        counts = _count_defs(ast.parse(source, filename=file_path))
        for name, expected_count in expected.items():
            assert counts.get(name, 0) == expected_count, (
                f"{file_path}: expected {expected_count} definition(s) of {name}, "
                f"found {counts.get(name, 0)}"
            )
