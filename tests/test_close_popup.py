from playwright.sync_api import sync_playwright
import sys
import os

# ✅ Add project root to sys.path *BEFORE* your local import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.home_page import HomePage  # ✅ NOW this will work

def test_close_login_popup():
    os.makedirs("results", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        home = HomePage(page)
        home.goto()
        home.close_login_popup()

        html_content = page.content()
        with open("results/page_after_close.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        browser.close()