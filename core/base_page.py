from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)

    # найти элемент
    def find(self, selector: str) -> Locator:
        return self.page.locator(selector)

    # кликнуть на элемент
    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    # заполнить элемент
    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    # нажать клавишу
    def press(self, selector: str, key: str) -> None:
        self.page.locator(selector).press(key)

    # ожидаем видимости элемента
    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    # посчитать количество элементов
    def count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    # сравнить текст элемента
    def compare_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_contain_text(text)

    # сравнить значение элемента
    def compare_value(self, selector: str, value: str) -> None:
        expect(self.page.locator(selector)).to_have_value(value)

    # сравнить атрибут элемента
    def compare_attribute(self, selector: str, attribute: str, value: str) -> None:
        expect(self.page.locator(selector)).to_have_attribute(attribute, value)

    # ожидаем включенности элемента
    def expect_enabled(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_enabled()

    # ожидаем отключенности элемента
    def expect_disabled(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_disabled()

    # ожидаем включенности элемента
    def expect_checked(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_checked()

    # ожидаем отключенности элемента
    def expect_unchecked(self, selector: str) -> None:
        expect(self.page.locator(selector)).not_to_be_checked()

