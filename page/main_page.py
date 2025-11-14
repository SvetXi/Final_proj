from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage
from .search_page import SearchPage
from config.test_data import test_data

class MainPage(BasePage):
    # Локаторы
    SEARCH_INPUT = ("css selector", "input[type='search']")
    SEARCH_BUTTON = ("css selector", "button[type='submit']")
    USER_PROFILE = ("css selector", ".user-profile")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Открыть главную страницу")
    def open(self):
        super().open("/")
        self.wait_for_page_load()
    
    @allure.step("Выполнить поиск товара: {query}")
    def search_for_product(self, query: str = test_data.SEARCH_QUERY):
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        allure.attach(f"Searched for: {query}", "Search", allure.attachment_type.TEXT)
        return SearchPage(self.driver)
    
    @allure.step("Проверить авторизацию пользователя")
    def is_user_logged_in(self) -> bool:
        return self.is_visible(self.USER_PROFILE)