import random

from playwright.sync_api import Page

from pages.eventswidget_page import EventsWidgetPage
from core.constants import *


# загрузка станицы
def test_eventswidget_loads(page: Page) -> None:
    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")
    home.expect_visible(home.locators["main_banner"])

# сравнивоем колл выбранных тем
def test_topic_checkboxes_counter(page: Page) -> None:
    topics = ["affiliate", "blockchain", "development", "igaming", "marketing", "SEO", "fintech"]

    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")
    home.check_number_checkboxes(0)
    home.click(home.locators["selection_counter_topic"])

    for topic in topics:
        home.click(home.locators[f"topic_{topic}"])
        checked_count = home.count(home.locators["checked_topics"])
        home.click(home.locators["selection_counter_topic"])
        home.check_number_checkboxes(checked_count)
        home.click(home.locators["selection_counter_topic"])
    home.click(home.locators["clear_topics"])
    home.check_number_checkboxes(0)
 
# проверяем дефолтные параметры
def test_default_parameters(page: Page) -> None:
    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")
    home.compare_text(home.locators["selection_counter_topic"], choose_a_topic)
    home.compare_text(home.locators["selection_counter_country"], all_countries)
    home.compare_value(home.locators["width_input"], width_input)
    home.expect_enabled(home.locators["full_width_checkbox"])
    home.compare_value(home.locators["height_input"], height_input)
    home.expect_enabled(home.locators["full_height_checkbox"])
    home.expect_checked(home.locators["theme_turquoise"])
    home.expect_unchecked(home.locators["theme_purple"])
    home.compare_text(home.locators["block_code"], default_block_code)

# проверяем минимальную ширину
def test_minimum_width(page: Page) -> None:
    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")

    for value in random.sample(range(1, 230), 10):
        home.fill(home.locators["width_input"], str(value))
        home.press(home.locators["width_input"], "Enter")
        home.compare_value(home.locators["width_input"], width_input)

# проверяем минимальную высоту
def test_minimum_height(page: Page) -> None:
    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")

    for value in random.sample(range(1, 240), 10):
        home.fill(home.locators["height_input"], str(value))
        home.press(home.locators["height_input"], "Enter")
        home.compare_value(home.locators["height_input"], height_input)


# проверяем максимальную ширину
def test_maximum_width(page: Page) -> None:
    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")

    for value in random.sample(range(1021, 9999), 10):
        home.fill(home.locators["width_input"], str(value))
        home.press(home.locators["width_input"], "Enter")
        home.compare_value(home.locators["width_input"], max_width)

# проверяем максимальную высоту
def test_maximum_height(page: Page) -> None:
    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")

    for value in random.sample(range(720, 9999), 10):
        home.fill(home.locators["height_input"], str(value))
        home.press(home.locators["height_input"], "Enter")
        home.compare_value(home.locators["height_input"], max_height)

# проверяем генерацию параметров
def test_generation_parameters(page: Page) -> None:
    topics = {
        "affiliate": "#Affiliate",
        "blockchain": "#Blockchain",
        "development": "#Development",
        "igaming": "#Igaming",
        "marketing": "#Internet Marketing",
        "SEO": "#SEO",
        "fintech": "#Fintech",
    }
    themes = ["theme_blue", "theme_green", "theme_turquoise", "theme_purple"]

    home = EventsWidgetPage(page)
    home.goto("/eventswidget/")

    chosen_topic_key, chosen_topic_name = random.choice(list(topics.items()))
    home.click(home.locators["selection_counter_topic"])
    home.click(home.locators[f"topic_{chosen_topic_key}"])
    home.click(home.locators["selection_counter_topic"])

    width = str(random.randint(230, 1020))
    home.fill(home.locators["width_input"], width)
    home.press(home.locators["width_input"], "Enter")

    height = str(random.randint(240, 720))
    home.fill(home.locators["height_input"], height)
    home.press(home.locators["height_input"], "Enter")

    chosen_theme = random.choice(themes)
    home.click(home.locators[chosen_theme])

    home.click(home.locators["preview_button"])
    home.check_all_generation_params(
        theme=chosen_theme.split("_")[1],
        width=width,
        height=height,
        topic=chosen_topic_name,
    )
