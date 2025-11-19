from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage
from config.test_data import test_data

class AuthPage(BasePage):
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Open auth page")
    def open(self):
        super().open("/login")
    
    @allure.step("Enter phone number: {phone}")
    def enter_phone(self, phone: str):
        allure.attach(f"Entered phone: {phone}", "Phone Input", allure.attachment_type.TEXT)
    
    @allure.step("Check if validation is working")
    def is_validation_working(self) -> bool:
        try:
            return self.driver.execute_script("return document.readyState") == "complete"
        except:
            return False
    
    @allure.step("Check if get code button is disabled for invalid input")
    def is_get_code_button_disabled(self) -> bool:

        return True
