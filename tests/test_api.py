import pytest
import allure
import sys
import os
from config.settings import settings
from config.test_data import test_data
from utils.api_client import ApiClient

auth_header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQxNTExNzEsImlhdCI6MTc2Mzk4MzE3MSwiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6ImZlMzZhYWI5M2FiZjk4ZGQ1ZWYwM2Q2MjEzYjlmOTQ4ZWZmY2E4ZWYwZDU1MzEzZWYxNjRmNjBhNDZmZmIyOTUiLCJ0eXBlIjoxMH0.36Bc3NpQLcildyBP0v4wfs-qVDxtRg915o1jGRuZIQ0"

api_client = ApiClient()


@allure.title("TC-1: Поиск с кириллическими символами")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_cyrillic_without_auth():
    with allure.step("Отправить запрос на кириллице"):
        response = api_client.facet_search(
            phrase=test_data.SEARCH_PHRASES["cyrillic"],
            headers={"Authorization": f"Bearer {auth_header}"}
        )

    with allure.step("Проверить статус ответа"):
        assert response.status_code == 200, f"204 No Content {response.status_code}"


@allure.title("TC-2: Поиск с использованием латинских символов")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_latin_without_auth():
    with allure.step("Отправить поисковый запрос с латинской фразой"):
        response = api_client.facet_search(
            phrase=test_data.SEARCH_PHRASES["latin"],
            headers={"Authorization": f"Bearer {auth_header}"}
        )

    with allure.step("Проверить статус ответа"):
        assert response.status_code == 200, f"204 No Content {response.status_code}"


@allure.title("TC-4: Поиск с специальными символами — ошибка проверки")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_special_chars():
    with allure.step("Отправить поисковый запрос с специальными символами"):
        response = api_client.facet_search(
            phrase=test_data.SEARCH_PHRASES["special_chars"],
            headers={"Authorization": f"Bearer {auth_header}"}
        )

    with allure.step("Проверить статус ответа"):
        assert response.status_code == 422, f"422 Unprocessable Content {response.status_code}"


@allure.title("TC-5: Поиск с фразой на кириллице и цифры")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_empty_phrase():
    with allure.step("Отправить поисковый запрос с кириллицей и цифрами"):
        response = api_client.facet_search(
            phrase=test_data.SEARCH_PHRASES["cyrillic plus numbers"],
            headers={"Authorization": f"Bearer {auth_header}"}
        )

    with allure.step("Проверить статус ответа"):
        assert response.status_code == 200, f"204 No Content {response.status_code}"


@allure.title("TC-6: Проверка поиска по цифрам")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_with_different_client():
    with allure.step("Отправить запрос с цифрами"):
        response = api_client.facet_search(
            phrase=test_data.SEARCH_PHRASES["numbers"],
            headers={"Authorization": f"Bearer {auth_header}"}
        )

    with allure.step("Проверить согласованное поведение"):
        assert response.status_code == 200, f"204 No Content {response.status_code}"
