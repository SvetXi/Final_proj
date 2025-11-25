import pytest
from selenium import webdriver
import allure
from page.search_page import SearchPage


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def search_page(driver):
    page = SearchPage(driver)
    page.open("https://www.chitai-gorod.ru/")
    return page


@allure.epic("UI Тестирование")
@allure.feature("Поиск книг")
@allure.title("Поиск книги по заголовку")
@allure.description(
    "Тест проверяет возможность поиска книги по заголовку "
    "'Технология сварочных работ'.")
def test_search_book_by_title(search_page):
    with allure.step("Ввести запрос на поиск книги по названию"):
        search_page.enter_search_query("Технология сварочных работ")
    with allure.step("Нажать кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получить заголовки продуктов"):
        product_titles = search_page.get_product_titles()
    assert any("Технология сварочных работ"
               in title for title in product_titles
               ), "Название книги не найдено в списке продуктов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книг")
@allure.title("Поиск автора")
@allure.description(
    "Тест проверяет возможность поиска автора 'Пелевин'.")
def test_search_author(search_page):
    with allure.step("Ввести запрос на поиск книги по автору"):
        search_page.enter_search_query("Пелевин")
    with allure.step("Нажать кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получить заголовки авторов"):
        product_titles = search_page.get_product_titles()
    assert len(product_titles) > 0, "Нет результатов поиска для автора"
    assert any("Пелевин" in title for title in product_titles
               ), "Имя автора не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск автора на английском языке")
@allure.description("Тест проверяет возможность поиска автора" \
                    " с опечаткой 'Леромнтов'.")
def test_search_author_in_english(search_page):
    with allure.step("Введите запрос для поиска"):
        search_page.enter_search_query("Леромнтов")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки продуктов"):
        product_titles = search_page.get_product_titles()
    assert len(product_titles) > 0, "Нет результатов поиска для автора"
    assert any(
        "Лермонтов" in title for title in product_titles
    ), "Фамилия автора не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск автора на английском языке")
@allure.description("Тест проверяет возможность поиска автора 'Lermontov'.")
def test_search_author_in_english(search_page):
    with allure.step("Введите запрос для поиска"):
        search_page.enter_search_query("Lermontov")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки продуктов"):
        product_titles = search_page.get_product_titles()
    assert len(product_titles) > 0, "Нет результатов поиска для автора"
    assert any(
        "Lermontov" in title for title in product_titles
    ), "Фамилия автора не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск книги с дефисом")
@allure.description("Тест проверяет возможность поиска книги 'Норд-Ост'.")
def test_search_book_with_hyphen(search_page):
    with allure.step("Введите запрос для поиска книги"):
        search_page.enter_search_query("Норд-Ост")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки продуктов"):
        product_titles = search_page.get_product_titles()
    assert len(product_titles) > 0, "Нет результатов поиска для книги"
    assert any(
        "Норд-Ост" in title for title in product_titles
    ), "Книга не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск с использованием только знаков препинания")
@allure.description("Тест проверяет обработку поиска, "
                    "состоящего только из знаков препинания.")
def test_search_punctuation_only(search_page):
    with allure.step("Введите запрос с знаками препинания"):
        search_page.enter_search_query(",,,….!!!")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Проверьте сообщение об отсутствии результатов"):
        message_text = search_page.check_no_results_message()
    assert (
            "Но на всякий случай советуем "
            "проверить опечатки в запросе." in message_text
    ), "Сообщение об отсутствии результатов не отображается."
