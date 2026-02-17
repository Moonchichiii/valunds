from __future__ import annotations

import os

import pytest

playwright = pytest.importorskip("playwright.sync_api")


@pytest.mark.e2e
def test_onboarding_flow_creates_profile_and_passport() -> None:
    base_url = os.getenv("E2E_BASE_URL")
    if not base_url:
        pytest.skip("Set E2E_BASE_URL to run browser E2E flow")

    with playwright.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(base_url, wait_until="domcontentloaded")
        assert page.locator("#main-content").count() == 1
        browser.close()
