choose_a_topic = "Выбрать тематику"
all_countries = "Все страны"
width_input = "230"
max_width = "1020"
height_input = "240"
max_height = "720"
default_block_code = """
<iframe id="3snet-frame" 
src="https://3snet.info/widget-active-events/?theme=turquoise&event_group=10622&event_type=&event_country=" 
width="230" height="240" frameborder="0"></iframe> 
"""

# список тестов для запуска из веб-интерфейса
LIST_TESTS = [
    "test_eventswidget_loads",
    "test_topic_checkboxes_counter",
    "test_default_parameters",
    "test_minimum_width",
    "test_minimum_height",
    "test_maximum_width",
    "test_maximum_height",
    "test_generation_parameters",
    # "test_test_error"
]
