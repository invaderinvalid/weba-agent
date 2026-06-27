from playwright.sync_api import sync_playwright
import json

class BrowserState:
    def __init__(self):
        # Start Playwright and open a visible browser window
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def navigate(self, url: str) -> str:
        """The actual Python function the agent will trigger."""
        print(f"🌍 Action: Navigating to {url}...")
        try:
            self.page.goto(url, timeout=15000)
            return f"Successfully navigated to {url}. The page title is '{self.page.title()}'."
        except Exception as e:
            return f"Error navigating to {url}: {str(e)}"

    def get_page_content(self) -> str:
        print("👁️ Action: Extracting page content...")
        try:
            content = self.page.locator("body").inner_text()
            return f"Page Content:\n{content[:2000]}..."
        except Exception as e:
            return f"Error extracting content: {str(e)}"
        

