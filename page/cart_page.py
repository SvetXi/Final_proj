from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage

class CartPage(BasePage):
    # Локаторы
    CART_ITEMS = ("css selector", ".cart-item")
    PRODUCT_NAMES = ("css selector", ".cart-item .product-name")
    EMPTY_CART_MESSAGE = ("css selector", ".empty-cart")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Открыть страницу корзины")
    def open(self):
        super().open("/cart")
        self.wait_for_page_load()
    
    @allure.step("Проверить наличие товара в корзине: {product_name}")
    def is_product_in_cart(self, product_name: str) -> bool:
        product_elements = self.find_elements(self.PRODUCT_NAMES)
        for element in product_elements:
            if product_name.lower() in element.text.lower():
                allure.attach(f"Found product in cart: {element.text}", "Cart Check", allure.attachment_type.TEXT)
                return True
        return False
    
    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        return len(self.find_elements(self.CART_ITEMS))