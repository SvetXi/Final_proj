import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.api_client import APIClient
from config.settings import settings
from page.auth_page import AuthPage
from page.main_page import MainPage
from page.search_page import SearchPage
from page.cart_page import CartPage

@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
        
    yield driver

    driver.quit()

class BasePage:
    def __init__(self, driver):
        self.driver = driver

class AuthPage(BasePage):
    def enter_phone(self, phone_number: str):
        el = self.driver.find_element("id", "phone_input")
        el.clear()
        el.send_keys(phone_number)

    def click_send_code(self):
        self.driver.find_element("id", "send_code_btn").click()

    def is_sms_code_input_visible(self) -> bool:
        try:
            el = self.driver.find_element("id", "sms_code_input")
            return el.is_displayed()
        except Exception:
            return False

class MainPage(BasePage):
    pass

class SearchPage(BasePage):
    pass

class CartPage(BasePage):
    pass

@pytest.fixture
def auth_page(driver):
    return AuthPage(driver)

@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@pytest.fixture
def search_page(driver):
    return SearchPage(driver)

@pytest.fixture
def cart_page(driver):
    return CartPage(driver)
# Хуки для Allure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Добавляем скриншот при падении теста
        try:
            if 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                screenshot = driver.get_screenshot_as_png()
                allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
                
                # Также добавляем HTML страницы
                page_source = driver.page_source
                allure.attach(page_source, name="page_source", attachment_type=allure.attachment_type.HTML)
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
