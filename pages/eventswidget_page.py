from playwright.sync_api import Page, expect

from core.base_page import BasePage
from core.constants import choose_a_topic


class EventsWidgetPage(BasePage):
    locators = {
        "main_banner": ".banners-header",
        "selection_counter_topic": "[data-select='Выбрать тематику']",
        "selection_counter_country": "[data-select='Все страны']",

        "width_input": 'input[name="width"]',
        "full_width_checkbox": 'input[name="full-width"]',
        "height_input": 'input[name="height"]',
        "full_height_checkbox": 'input[name="auto-height"]',

        "theme_blue": 'label:has(input[name="theme"][value="blue"]) .theme-round',
        "theme_green": 'label:has(input[name="theme"][value="green"]) .theme-round',
        "theme_turquoise": 'label:has(input[name="theme"][value="turquoise"]) .theme-round',
        "theme_purple": 'label:has(input[name="theme"][value="purple"]) .theme-round',

        "theme_turquoise_checked": 'input[name="theme"][value="turquoise"]',
        "theme_purple_checked": 'input[name="theme"][value="purple"]',

        "block_code": "textarea#code",
        "preview_button": "button.button.green-bg:has-text('Сгенерировать превью')",
        "preview_iframe": 'iframe[id="3snet-frame"]',

        "all_topics": "[data-select='Выбрать тематику'] .checkselect-popup label:has(input.selectAll)",
        "topic_affiliate": "[data-select='Выбрать тематику'] .checkselect-popup label.custom-checkbox:has-text('Affiliate')",
        "topic_blockchain": "[data-select='Выбрать тематику'] .checkselect-popup label.custom-checkbox:has-text('Blockchain')",
        "topic_development": "[data-select='Выбрать тематику'] .checkselect-popup label.custom-checkbox:has-text('Development')",
        "topic_igaming": "[data-select='Выбрать тематику'] .checkselect-popup label.custom-checkbox:has-text('Igaming')",
        "topic_marketing": "[data-select='Выбрать тематику'] .checkselect-popup label.custom-checkbox:has-text('Internet Marketing')",
        "topic_SEO": "[data-select='Выбрать тематику'] .checkselect-popup label.custom-checkbox:has-text('SEO')",
        "topic_fintech": "[data-select='Выбрать тематику'] .checkselect-popup label.custom-checkbox:has-text('Финтех')",

        "selected_checkbox": ".checkselect-control .active",
        "checked_topics": "[data-select='Выбрать тематику'] .checkselect-popup input[type='checkbox']:not(.selectAll):checked",
        "clear_topics": '.checkselect-clear[data-name="type"]:has-text("Очистить")',
        "clear_countries": '.checkselect-clear[data-name="country"]:has-text("Очистить")',
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # проверяем количество выбранных чекбоксов
    def check_number_checkboxes(self, number: int) -> None:
        if number == 0:
            self.compare_text(self.locators["selection_counter_topic"], choose_a_topic)
        else:
            self.compare_text(self.locators["selection_counter_topic"], f"Выбрано: {number}")

    # проверяем параметры кода
    def check_code_params(self, theme: str, width: str, height: str) -> None:
        self.compare_text(self.locators["block_code"], f"theme={theme}")
        self.compare_text(self.locators["block_code"], f'width="{width}"')
        self.compare_text(self.locators["block_code"], f'height="{height}"')

    # проверяем параметры превью
    def check_preview_params(self, theme: str, width: str, height: str) -> None:
        src = self.page.locator(self.locators["preview_iframe"]).get_attribute("src")
        assert f"theme={theme}" in src
        self.compare_attribute(self.locators["preview_iframe"], "width", width)
        self.compare_attribute(self.locators["preview_iframe"], "height", height)

    # проверяем тему в превью
    def check_preview_topic(self, topic: str) -> None:
        frame = self.page.frame_locator(self.locators["preview_iframe"])
        expect(frame.locator(".event-type")).to_contain_text(topic)

    # проверяем все параметры генерации
    def check_all_generation_params(self, theme: str, width: str, height: str, topic: str) -> None:
        self.check_code_params(theme, width, height)
        self.check_preview_params(theme, width, height)
