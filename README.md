# Autotests Project

Проект автоматизации UI и API тестов для сайта Читай-город.

### Шаги
1. Установить зависимости
2. Запустить тесты 'pytest'
3. Сгенерировать отчет 'allure generate allure-files -o allure-report'
4. Открыть отчет 'allure open allure-report'

### Стек:
- pytest
- selenium
- requests
- allure

### Струткура:
- ./test - тесты
- ./pages - описание страниц
- ./api - хелперы для работы с API


### Библиотеки (!)
- pip install pytest
- pip install selenium
- pip install webdriver-manager 
- pip install allure-pytest
