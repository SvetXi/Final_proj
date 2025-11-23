import requests
import allure
from config.settings import settings
from typing import Optional

class APIClient:
    def __init__(self, base_url: str = settings.BASE_API_URL):
        self.base_url = base_url
        self.session = requests.Session()
    def init(self, base_url: str, token: Optional[str] = None, timeout: float = 10.0):
        self.timeout = timeout
        self.token = token or self._load_token_from_env()
        if not self.token:
            raise ValueError("API token must be provided either via parameter or environment variable.")
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}
    
    @allure.step("Execute facet search")
    def facet_search(self, phrase: str):
        url = f"{self.base_url}/search/facet-search"
        params = {
            "customerCityId": settings.CUSTOMER_CITY_ID,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP
        }
        return self.session.get(url, params=params, timeout=settings.API_TIMEOUT)
    
    @allure.step("Execute search suggests")
    def search_suggests(self, phrase: str):
        url = f"{self.base_url}/search/search-phrase-suggests"
        params = {
            "suggests[page]": 1,
            "suggests[per-page]": 5,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP
        }
        return self.session.get(url, params=params, timeout=settings.API_TIMEOUT)
