import requests
import allure
from config.settings import settings
from typing import Optional

class ApiClient:

    def setup_method(self):
        self.api_client = ApiClient(base_url="https://web-agr.chitai-gorod.ru/web/api/v2/search/facet-search")

    def get(self, path: str, **kwargs):
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        headers = kwargs.pop("headers", {})
        headers.update(self._authorized_headers())
        return self.session.get(url, headers=headers, **kwargs)

    def post(self, path: str, json=None, data=None, **kwargs):
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        headers = kwargs.pop("headers", {})
        headers.update(self._authorized_headers())
        return self.session.post(url, url=url, json=json, data=data, headers=headers, **kwargs)

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
