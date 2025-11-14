from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage
from config.test_data import test_data

class AuthPage(BasePage):
    # Локаторы 
    PHONE_INPUT = ("css selector", "input[type='tel'], input[name='phone'], input[placeholder*='телефон']")
    GET_CODE_BUTTON = ("xpath", "//button[contains(text(), 'Получить код') or contains(text(), 'Получить смс')]")
    SMS_CODE_INPUT = ("css selector", "input[type='text'], input[name='code'], input[placeholder*='код']")
    SUBMIT_CODE_BUTTON = ("xpath", "//button[contains(text(), 'Войти') or contains(text(), 'Продолжить')]")
    ERROR_MESSAGE = ("css selector", ".error, .error-message, [class*='error']")
    SUCCESS_INDICATOR = ("css selector", ".profile, .account, [class*='user']")
    LOADING_SPINNER = ("css selector", ".spinner, .loading, [class*='loading']")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Открыть страницу авторизации")
    def open(self):
        super().open(test_data.AUTH_URL)
        self.wait_for_page_load()
        self.find_element(self.PHONE_INPUT)
    
    @allure.step("Ввести номер телефона: {phone}")
    def enter_phone(self, phone: str = test_data.VALID_PHONE):
        self.input_text(self.PHONE_INPUT, phone)
        allure.attach(f"Entered phone: {phone}", "Input", allure.attachment_type.TEXT)
    
    @allure.step("Нажать кнопку получения кода")
    def click_get_code(self):
        self.click(self.GET_CODE_BUTTON)
        if self.is_visible(self.LOADING_SPINNER, timeout=2):
            self.wait_for_element_to_disappear(self.LOADING_SPINNER)
    
    @allure.step("Проверить видимость поля для SMS кода")
    def is_sms_code_input_visible(self) -> bool:
        return self.is_visible(self.SMS_CODE_INPUT, timeout=10)
    
    @allure.step("Ввести SMS код: {code}")
    def enter_sms_code(self, code: str = test_data.SMS_CODE):
        if self.is_sms_code_input_visible():
            self.input_text(self.SMS_CODE_INPUT, code)
            original_url = self.get_current_url()
            self.click(self.SUBMIT_CODE_BUTTON)

            try:
                self.wait_for_url_change(original_url, timeout=5)
            except TimeoutException:
                if not self.is_authorization_successful():
                    raise Exception("Authorization failed - no URL change and no success indicator")
            
            allure.attach(f"Entered SMS code: {code}", "Input", allure.attachment_type.TEXT)
        else:
            raise Exception("SMS code input is not visible")
    
    @allure.step("Проверить успешную авторизацию")
    def is_authorization_successful(self) -> bool:
        current_url = self.get_current_url()
        url_success = test_data.AUTH_URL not in current_url
        element_success = self.is_visible(self.SUCCESS_INDICATOR, timeout=3)
        
        return url_success or element_success
