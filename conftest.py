import pytest
from playwright.sync_api import Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://dev.3snet.info/"


@pytest.fixture
def context(browser: Browser, base_url: str) -> BrowserContext:
    ctx = browser.new_context(base_url=base_url)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()
