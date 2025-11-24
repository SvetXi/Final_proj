import requests
import allure
from config.settings import settings
from typing import Optional

  # Конфигурация
AUTH_URL = "https://web-agr.chitai-gorod.ru/web/api/v2"  
CLIENT_ID = "tid_chitaigorod"
CLIENT_SECRET = "secret"

API_BASE_URL = "https://web-agr.chitai-gorod.ru/web/api/v2"

class TokenManager:
    def __init__(self, auth_url: str, client_id: str, client_secret: str):
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: Optional[str] = None
        self._expires_at: Optional[float] = None

    def _is_expired(self) -> bool:
        if self._token is None or self._expires_at is None:
            return True

    def _fetch_token(self) -> None:
        data = {
            "grant_type": "client_credentials"
        }
        auth = (self.client_id, self.client_secret)

        resp = requests.post(self.auth_url, data=data, auth=auth)
        resp.raise_for_status()
        payload = resp.json()

        # ожидаемые поля: access_token и expires_in (в секундах)
        access_token = payload.get("access_token")
        expires_in = payload.get("expires_in", 3600)

        if not access_token:
            raise RuntimeError(format(payload))

        self._token = access_token

    def get_token(self) -> str:
        if self._is_expired():
            self._fetch_token()
        if not self._token:
            raise RuntimeError("Token не инициализирован")
        return self._token

class ApiClient:
    def __init__(self, base_url: str, token_manager: TokenManager):
        self.base_url = base_url
        self.token_manager = token_manager
        self.session = requests.Session()

    def _authorized_headers(self) -> dict:
        token = self.token_manager.get_token()
        return {"Authorization": f"Bearer {token}"}

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
