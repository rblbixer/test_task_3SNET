from playwright.sync_api import Page

from core.base_page import BasePage


class HomePage(BasePage):
    locators = {
        "main_banner": ".banners-header",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    
