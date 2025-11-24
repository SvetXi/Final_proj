from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Helpers:
    @staticmethod
    def wait_for_element(driver: WebDriver, locator: tuple, timeout: int = 10):
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
