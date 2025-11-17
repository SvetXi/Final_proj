import requests
import allure
from config.settings import settings
from utils.helpers import helpers

class APIClient:
    def __init__(self, base_url: str = settings.BASE_API_URL, auth_token: str = None):
        self.base_url = base_url
        self.session = requests.Session()
        if auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})
    
    @allure.step("Выполнить facet search")
    def facet_search(self, phrase: str, customer_city_id: int = settings.CUSTOMER_CITY_ID):
        url = f"{self.base_url}/search/facet-search"
        params = {
            "customerCityId": customer_city_id,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP
        }
        response = self.session.get(url, params=params, timeout=settings.API_TIMEOUT)
        allure.attach(helpers.format_response_for_logging(response), "Response", allure.attachment_type.JSON)
        return response
    
    @allure.step("Выполнить search suggests")
    def search_suggests(self, phrase: str, customer_city_id: int = settings.CUSTOMER_CITY_ID):
        url = f"{self.base_url}/search/search-phrase-suggests"
        params = {
            "suggests[page]": 1,
            "suggests[per-page]": 5,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP,
            "include": "authors,bookCycles,categories,publishers,publisherSeries,products"
        }
        response = self.session.get(url, params=params, timeout=settings.API_TIMEOUT)
        allure.attach(helpers.format_response_for_logging(response), "Response", allure.attachment_type.JSON)
        return response
