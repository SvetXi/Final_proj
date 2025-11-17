import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.api_client import APIClient
from config.settings import settings
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage

@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()

@pytest.fixture(scope="function")
def driver():
    """Фикстура для веб-драйвера"""
    driver = None
    try:
        if settings.BROWSER.lower() == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            if settings.HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(service=service, options=options)
        
        elif settings.BROWSER.lower() == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            options = webdriver.FirefoxOptions()
            if settings.HEADLESS:
                options.add_argument("--headless")
            driver = webdriver.Firefox(service=service, options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {settings.BROWSER}")
        
        driver.implicitly_wait(settings.IMPLICIT_WAIT)
        driver.maximize_window()
        
        yield driver
        
    except Exception as e:
        print(f"Error initializing driver: {e}")
        raise
    finally:
        if driver:
            driver.quit()

@pytest.fixture
def auth_page(driver):
    """Фикстура для страницы авторизации"""
    return AuthPage(driver)

@pytest.fixture
def main_page(driver):
    """Фикстура для главной страницы"""
    return MainPage(driver)

@pytest.fixture
def search_page(driver):
    """Фикстура для страницы поиска"""
    return SearchPage(driver)

@pytest.fixture
def cart_page(driver):
    """Фикстура для страницы корзины"""
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
