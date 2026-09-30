"""Render the share card: python scripts/render_og.py (requires Playwright Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    page.goto((root / "scripts/og-image.html").as_uri(), wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    assert page.evaluate("Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
    assert page.evaluate("document.documentElement.scrollHeight === 630")
    page.screenshot(path=str(root / "assets/og-image.png"))
    browser.close()
print("Rendered assets/og-image.png (1200 × 630)")
