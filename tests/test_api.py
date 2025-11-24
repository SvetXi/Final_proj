import pytest
import allure
import sys
import os
from config.settings import settings
from config.test_data import test_data
from utils.api_client import ApiClient


@allure.feature("API Search Tests")
class TestAPISearch:

    def setup_method(self):

        self.api_client = ApiClient()
    
    @allure.title("TC-1: Поиск с кириллическими символами")
    @allure.severity(allure.severity_level.CRITICAL)


    def test_search_cyrillic_without_auth(self):
        return {"Authorization": "Bearer token"}

        headers = {
        "Authorization": auth_header,
    }
    
        with allure.step("Отправить запрос на кириллице"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["cyrillic"]
            )
        
        with allure.step("Проверить статус ответа"):
            assert response.status_code == 204, f"204 No Content {response.status_code}"

    
    @allure.title("TC-2: Поиск с использованием латинских символов") 
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_latin_without_auth(self):
        return {"Authorization": "Bearer token"}

        headers = {
        "Authorization": auth_header,
    }

        with allure.step("Отправить поисковый запрос с латинской фразой"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["latin"]
            )
        
        with allure.step("Проверить статус ответа"):
            assert response.status_code == 204, f"204 No Content"
            

    
    @allure.title("TC-4: Поиск с специальными символами — ошибка проверки")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_special_chars(self):
        return {"Authorization": "Bearer token"}

        headers = {
        "Authorization": auth_header,
    }
        with allure.step("Отправить поисковый запрос с специальными символами"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["special_chars"]
            )
        
        with allure.step("Проверить статус ответа"):
            assert response.status_code == 422, f"422 Unprocessable Content"
    
    @allure.title("TC-5: Поиск с фразой на кириллице и цифры")
    @allure.severity(allure.severity_level.CRITICAL) 
    def test_search_empty_phrase(self):
        return {"Authorization": "Bearer token"}

        headers = {
        "Authorization": auth_header,
    }
        with allure.step("Отправить поисковый запрос с специальными символами"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["cyrillic plus numbers"]
            )
        
        with allure.step("Проверить статус ответа"):
            assert response.status_code == 204, f"204 No Content"
    @allure.title("TC-6: Проверка поиска по цифрам")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_with_different_client(self):
        return {"Authorization": "Bearer token"}

        headers = {
        "Authorization": auth_header,
    }
        with allure.step("Запрос только с цифрами"):
            new_client = ApiClient()
        
        with allure.step("Отправить запрос с цифрами"):
            response = self.api_client.facet_search(
                phrase=test_data.SEARCH_PHRASES["numbers"]
            )
        
        with allure.step("Verify consistent behavior"):
            assert response.status_code == 204, f"204 No Content {response.status_code}"
