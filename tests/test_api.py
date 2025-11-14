import pytest
import requests
import allure
from config.settings import settings
from config.test_data import test_data

@allure.feature("API Search Tests")
class TestAPISearch:
    
    @allure.title("TC-1: Search with cyrillic characters")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_cyrillic(self, api_client):
        with allure.step("Send search request with cyrillic phrase"):
            response = api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["cyrillic"]
            )
        
        with allure.step("Verify response"):
            assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
            if response.status_code == 200:
                json_data = response.json()
                assert "data" in json_data, "Response should contain 'data' field"
                assert isinstance(json_data["data"], list), "Data should be a list"
    
    @allure.title("TC-2: Search with latin characters") 
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_latin(self, api_client):
        with allure.step("Send search request with latin phrase"):
            response = api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["latin"]
            )
        
        with allure.step("Verify response"):
            assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
            if response.status_code == 200:
                json_data = response.json()
                assert "data" in json_data, "Response should contain 'data' field"
    
    @allure.title("TC-4: Search with special characters - negative")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_special_chars(self, api_client):
        with allure.step("Send search request with special characters"):
            response = api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["special_chars"]
            )
        
        with allure.step("Verify error response"):
            assert response.status_code >= 400, f"Expected error status, got {response.status_code}"
            
            try:
                json_data = response.json()
                if "errors" in json_data:
                    errors_found = any(
                        test_data.ERROR_MESSAGES["invalid_phrase"] in error.get("title", "") 
                        for error in json_data["errors"]
                    )
                    assert errors_found, "Should contain invalid phrase error"
            except:
                assert response.status_code != 200, "Should not return 200 for invalid search"
    
    @allure.title("TC-5: Search with empty phrase - negative")
    @allure.severity(allure.severity_level.CRITICAL) 
    def test_search_empty_phrase(self, api_client):
        with allure.step("Send search request with empty phrase"):
            response = api_client.search_suggests(phrase="")
        
        with allure.step("Verify validation error"):
            assert response.status_code >= 400, f"Expected error status, got {response.status_code}"
            
            try:
                json_data = response.json()
                if "errors" in json_data:
                    empty_errors = any(
                        "пуст" in error.get("title", "").lower() 
                        for error in json_data["errors"]
                    )
                    assert empty_errors, "Should contain empty value error"
            except:
                assert response.status_code != 200, "Should not return 200 for empty search"
    
    @allure.title("TC-6: Search without auth token - negative")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_without_auth(self):
        with allure.step("Send search request without authorization"):
            url = f"{settings.BASE_API_URL}/search/facet-search"
            params = {
                "customerCityId": settings.CUSTOMER_CITY_ID,
                "phrase": test_data.SEARCH_PHRASES["cyrillic"],
                "abTestGroup": settings.AB_TEST_GROUP
            }
            response = requests.get(url, params=params, timeout=settings.API_TIMEOUT)
        
        with allure.step("Verify unauthorized error"):
            assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"
            
            try:
                json_data = response.json()
                auth_errors = any(
                    keyword in json_data.get("message", "").lower() 
                    for keyword in ["auth", "authorization", "token", "access"]
                )
                assert auth_errors, "Should contain authorization error"
            except:
                assert response.status_code in [401, 403]