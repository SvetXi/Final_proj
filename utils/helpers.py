import random
import string
import json
from datetime import datetime
from typing import Any, Dict, Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Helpers:
    """Вспомогательные функции для тестов"""
    
    @staticmethod
    def generate_random_phone() -> str:
        """Генерация случайного номера телефона"""
        return f"+79{random.randint(100000000, 999999999)}"
    
    @staticmethod
    def generate_random_email() -> str:
        """Генерация случайного email"""
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(['gmail.com', 'yahoo.com', 'mail.ru'])
        return f"{username}@{domain}"
    
    @staticmethod
    def wait_for_element(driver: WebDriver, locator: tuple, timeout: int = 10) -> bool:
        """Ожидание появления элемента"""
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_element_clickable(driver: WebDriver, locator: tuple, timeout: int = 10) -> bool:
        """Ожидание кликабельности элемента"""
        try:
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_element_visible(driver: WebDriver, locator: tuple, timeout: int = 10) -> bool:
        """Ожидание видимости элемента"""
        try:
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_element_invisible(driver: WebDriver, locator: tuple, timeout: int = 10) -> bool:
        """Ожидание исчезновения элемента"""
        try:
            WebDriverWait(driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_page_load(driver: WebDriver, timeout: int = 10):
        """Ожидание загрузки страницы"""
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    @staticmethod
    def wait_for_url_change(driver: WebDriver, original_url: str, timeout: int = 10):
        """Ожидание изменения URL"""
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.current_url != original_url
        )
    
    @staticmethod
    def wait_for_text_in_element(driver: WebDriver, locator: tuple, text: str, timeout: int = 10) -> bool:
        """Ожидание появления текста в элементе"""
        try:
            WebDriverWait(driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def safe_click(driver: WebDriver, locator: tuple, timeout: int = 10) -> bool:
        """Безопасный клик с обработкой исключений"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    @staticmethod
    def safe_send_keys(driver: WebDriver, locator: tuple, text: str, timeout: int = 10) -> bool:
        """Безопасный ввод текста"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    @staticmethod
    def format_response_for_logging(response) -> Dict[str, Any]:
        """Форматирование ответа API для логирования"""
        try:
            body = response.json() if response.content else None
        except:
            body = response.text
        
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
            "url": response.url,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def save_screenshot(driver: WebDriver, test_name: str) -> str:
        """Сохранение скриншота с уникальным именем"""
        import os
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        filename = f"{screenshots_dir}/{test_name}_{timestamp}.png"
        driver.save_screenshot(filename)
        return filename
    
    @staticmethod
    def retry_on_failure(func: Callable, max_attempts: int = 3, delay: int = 1):
        """Повторение функции при неудаче"""
        import time
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(delay)

helpers = Helpers()