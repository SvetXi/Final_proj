from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage
from .cart_page import CartPage
from config.test_data import test_data

class SearchPage(BasePage):
    # Локаторы
    SEARCH_RESULTS = ("css selector", ".product-card, .search-result, [class*='product']")
    AUTHOR_FILTER = ("xpath", f"//label[contains(., '{test_data.AUTHOR_FILTER}')]")
    FILTER_ACTIVE = ("css selector", ".filter-active, [class*='active']")
    FIRST_PRODUCT = ("css selector", ".product-card:first-child, .search-result:first-child")
    ADD_TO_CART_BUTTON = ("css selector", ".buy-button, .add-to-cart, [class*='cart']")
    PRODUCT_NAME = ("css selector", ".product-name, .title, [class*='name']")
    CART_ICON = ("css selector", ".cart-icon, .basket, [class*='cart']")
    CART_COUNTER = ("css selector", ".cart-counter, .basket-count, [class*='count']")
    LOADING_INDICATOR = ("css selector", ".loading, .spinner, [class*='load']")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Открыть страницу поиска с запросом: {query}")
    def open_with_query(self, query: str = test_data.SEARCH_QUERY):
        super().open(f"{test_data.SEARCH_URL}?query={query}")
        self.wait_for_page_load()
        self.wait_for_search_results()
    
    @allure.step("Ожидать появления результатов поиска")
    def wait_for_search_results(self, timeout: int = 10):
        """Ожидание появления результатов поиска"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.SEARCH_RESULTS)
            )
        except TimeoutException:

            pass
    
    @allure.step("Проверить отображение результатов поиска")
    def are_results_displayed(self) -> bool:
        return self.is_visible(self.SEARCH_RESULTS, timeout=5)
    
    @allure.step("Получить количество результатов")
    def get_results_count(self) -> int:
        if self.are_results_displayed():
            return len(self.find_elements(self.SEARCH_RESULTS))
        return 0
    
    @allure.step("Применить фильтр по автору: {author_name}")
    def apply_author_filter(self, author_name: str = test_data.AUTHOR_FILTER):
        original_count = self.get_results_count()
        self.click(self.AUTHOR_FILTER)
        
        
        if self.is_visible(self.LOADING_INDICATOR, timeout=2):
            self.wait_for_element_to_disappear(self.LOADING_INDICATOR)
        

        WebDriverWait(self.driver, 10).until(
            lambda driver: self.get_results_count() != original_count or not self.are_results_displayed()
        )
        
        allure.attach(f"Applied author filter: {author_name}", "Filter", allure.attachment_type.TEXT)
    
    @allure.step("Проверить применение фильтра: {filter_name}")
    def is_filter_applied(self, filter_name: str) -> bool:
        return self.is_visible(self.FILTER_ACTIVE)
    
    @allure.step("Получить название первого товара")
    def get_first_product_name(self) -> str:
        if self.are_results_displayed():
            return self.get_text(self.PRODUCT_NAME)
        return ""
    
    @allure.step("Добавить первый товар в корзину")
    def add_first_product_to_cart(self):
        if not self.are_results_displayed():
            raise Exception("No products available to add to cart")
        
        product_name = self.get_first_product_name()
        
        initial_cart_count = 0
        if self.is_visible(self.CART_COUNTER, timeout=2):
            initial_cart_count = int(self.get_text(self.CART_COUNTER) or 0)
        
        self.click(self.ADD_TO_CART_BUTTON)
        
        if self.is_visible(self.CART_COUNTER, timeout=3):
            WebDriverWait(self.driver, 10).until(
                lambda driver: int(self.get_text(self.CART_COUNTER) or 0) > initial_cart_count
            )
        
        allure.attach(f"Added to cart: {product_name}", "Cart", allure.attachment_type.TEXT)
        return product_name
    
    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        original_url = self.get_current_url()
        self.click(self.CART_ICON)
        
        self.wait_for_url_change(original_url)
        
        return CartPage(self.driver)