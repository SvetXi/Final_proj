import requests
from config.settings import settings

class APIClient:
    def __init__(self, base_url=settings.BASE_API_URL, auth_token=None):
        self.base_url = base_url
        self.session = requests.Session()
        if auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})
    
    def facet_search(self, phrase, customer_city_id=settings.CUSTOMER_CITY_ID):
        url = f"{self.base_url}/search/facet-search"
        params = {
            "customerCityId": customer_city_id,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP
        }
        return self.session.get(url, params=params, timeout=settings.API_TIMEOUT)
    
    def search_suggests(self, phrase, customer_city_id=settings.CUSTOMER_CITY_ID):
        url = f"{self.base_url}/search/search-phrase-suggests"
        params = {
            "suggests[page]": 1,
            "suggests[per-page]": 5,
            "phrase": phrase,
            "abTestGroup": settings.AB_TEST_GROUP,
            "include": "authors,bookCycles,categories,publishers,publisherSeries,products"
        }
        return self.session.get(url, params=params, timeout=settings.API_TIMEOUT)
