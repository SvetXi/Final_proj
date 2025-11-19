import pytest
import allure
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)

from config.settings import settings
from config.test_data import test_data
from utils.api_client import APIClient


@allure.feature("API Search Tests")
class TestAPISearch:

    
    def setup_method(self):

        self.api_client = APIClient()
    
    @allure.title("TC-1: Search with cyrillic characters without auth")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_cyrillic_without_auth(self):

        with allure.step("Send search request with cyrillic phrase without auth"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["cyrillic"]
            )
        
        with allure.step("Verify unauthorized response"):
            assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
            
            response_data = response.json()
            assert "message" in response_data, "Response should contain error message"
            assert "authorization" in response_data["message"].lower(), "Error should mention authorization"
    
    @allure.title("TC-2: Search with latin characters without auth") 
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_latin_without_auth(self):

        with allure.step("Send search request with latin phrase without auth"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["latin"]
            )
        
        with allure.step("Verify unauthorized response"):
            assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
            
            response_data = response.json()
            assert "message" in response_data, "Response should contain error message"
    
    @allure.title("TC-4: Search with special characters - validation error")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_special_chars(self):

        with allure.step("Send search request with special characters"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["special_chars"]
            )
        
        with allure.step("Verify validation error response"):
            assert response.status_code == 401, f"Expected 401 (auth required), got {response.status_code}"
    
    @allure.title("TC-5: Search with empty phrase - validation error")
    @allure.severity(allure.severity_level.CRITICAL) 
    def test_search_empty_phrase(self):

        with allure.step("Send search request with empty phrase"):
            response = self.api_client.search_suggests(phrase="")
        
        with allure.step("Verify validation error response"):
            assert response.status_code == 401, f"Expected 401 (auth required), got {response.status_code}"
    
    @allure.title("TC-6: Search with different client instance")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_with_different_client(self):

        with allure.step("Create new API client instance"):
            new_client = APIClient()
        
        with allure.step("Send search request with new client"):
            response = new_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["cyrillic"]
            )
        
        with allure.step("Verify consistent behavior"):
            assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
