"""Sanity checks to prevent regressions from bad merge artifacts."""

import importlib

import pytest

pytest.importorskip("django")

MODULES = [
    "accounts.models",
    "passports.models",
    "passports.selectors",
    "passports.services",
    "passports.views",
    "config.asgi",
]


def test_enterprise_modules_import_cleanly() -> None:
    for module_name in MODULES:
        module = importlib.import_module(module_name)
        assert module is not None
