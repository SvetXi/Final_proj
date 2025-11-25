import requests
import allure
from config.settings import settings
from typing import Optional


class ApiClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or "https://web-agr.chitai-gorod.ru/web/api/v2"
        self.session = requests.Session()

    def _authorized_headers(self):
        """Генерирует авторизационные заголовки"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }

    def get(self, path: str, **kwargs):
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        headers = kwargs.pop("headers", {})
        headers.update(self._authorized_headers())
        return self.session.get(url, headers=headers, **kwargs)

    def post(self, path: str, json=None, data=None, **kwargs):
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        headers = kwargs.pop("headers", {})
        headers.update(self._authorized_headers())
        return self.session.post(url, json=json, data=data, headers=headers, **kwargs)

    @allure.step("Execute facet search")
    def facet_search(self, phrase: str, headers: Optional[dict] = None):
        url = f"{self.base_url}/search/facet-search"
        params = {
            "customerCityId": settings.CUSTOMER_CITY_ID,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP
        }

        # Объединяем заголовки
        request_headers = self._authorized_headers()
        if headers:
            request_headers.update(headers)

        return self.session.get(url, params=params, headers=request_headers, timeout=settings.API_TIMEOUT)

    @allure.step("Execute search suggests")
    def search_suggests(self, phrase: str, headers: Optional[dict] = None):
        url = f"{self.base_url}/search/search-phrase-suggests"
        params = {
            "suggests[page]": 1,
            "suggests[per-page]": 5,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP
        }

        # Объединяем заголовки
        request_headers = self._authorized_headers()
        if headers:
            request_headers.update(headers)

        return self.session.get(url, params=params, headers=request_headers, timeout=settings.API_TIMEOUT)
