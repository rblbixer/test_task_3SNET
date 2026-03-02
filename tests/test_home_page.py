from playwright.sync_api import Page

from pages.home_page import HomePage


def test_home_page_loads(page: Page) -> None:
    home = HomePage(page)
    home.goto("/")
    home.expect_visible(home.locators["main_banner"])
