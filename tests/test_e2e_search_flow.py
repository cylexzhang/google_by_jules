from playwright.sync_api import Page, expect, sync_playwright
import os

# Define the directory for screenshots
SCREENSHOT_DIR = "tests/screenshots"

def test_search_flow(page: Page):
    """
    This test verifies that a user can perform a search and view the results.
    """
    # 1. Arrange: Go to the search homepage.
    page.goto("http://127.0.0.1:5000/")

    # 2. Act: Fill in the search input and click the search button.
    page.get_by_role("textbox", name="").fill("Playwright")
    page.get_by_role("button", name="Google Search").click()

    # 3. Assert: Confirm the navigation to the results page was successful
    # and that at least one search result is visible.
    expect(page).to_have_title("Google Search Results")
    # Wait for the first result item to appear, with a timeout of 10 seconds.
    page.wait_for_selector(".result-item", timeout=10000)

    # 4. Screenshot: Capture the final result for visual verification.
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_results.png"))

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_search_flow(page)
        finally:
            browser.close()
