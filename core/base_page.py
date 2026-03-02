from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()
