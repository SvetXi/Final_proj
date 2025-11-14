from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
from config.settings import settings
from utils.helpers import helpers

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = settings.BASE_UI_URL
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)
    
    @allure.step("Открыть страницу {path}")
    def open(self, path: str = ""):
        url = f"{self.base_url}{path}"
        self.driver.get(url)
        helpers.wait_for_page_load(self.driver)
        allure.attach(f"Opened URL: {url}", "Navigation", allure.attachment_type.TEXT)
    
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: tuple, timeout: int = None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator: tuple, timeout: int = None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))
    
    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator: tuple, timeout: int = None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def input_text(self, locator: tuple, text: str, timeout: int = None):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: tuple, timeout: int = None) -> str:
        element = self.find_element(locator, timeout)
        return element.text
    
    @allure.step("Проверить видимость элемента {locator}")
    def is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        return helpers.wait_for_element_visible(self.driver, locator, timeout)
    
    @allure.step("Ожидать загрузки страницы")
    def wait_for_page_load(self, timeout: int = 10):
        helpers.wait_for_page_load(self.driver, timeout)
    
    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url
    
    @allure.step("Ожидать изменения URL")
    def wait_for_url_change(self, original_url: str, timeout: int = 10):
        helpers.wait_for_url_change(self.driver, original_url, timeout)
    
    @allure.step("Ожидать появления текста '{text}' в элементе {locator}")
    def wait_for_text(self, locator: tuple, text: str, timeout: int = 10):
        helpers.wait_for_text_in_element(self.driver, locator, text, timeout)
    
    @allure.step("Ожидать исчезновения элемента {locator}")
    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = 10):
        helpers.wait_for_element_invisible(self.driver, locator, timeout)