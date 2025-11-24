import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    base_url = "https://web-agr.chitai-gorod.ru/web/api/v2/search/facet-search"
    API_TIMEOUT = 30
    TIMEOUT = 10
    
    # UI Settings
    BASE_UI_URL = "https://www.chitai-gorod.ru"
    BROWSER = "chrome"
    HEADLESS = True 
    
    # Wait settings
    IMPLICIT_WAIT = 5
    EXPLICIT_WAIT = 10
    
    # Test Data
    CUSTOMER_CITY_ID = 213
    AB_TEST_GROUP = 1

    # API Token
    def auth_header(cls) -> dict[str, str]:
        return {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIyNzY0MTUyLCJpYXQiOjE3NjQwMTYwNTYsImV4cCI6MTc2NDAxOTY1NiwidHlwZSI6MjAsImp0aSI6IjAxOWFiNzhjLWU5ODgtN2E3Yi1iYzgzLTM5N2RiNWEzMzljZiIsInJvbGVzIjoxMH0.MH-dLdNOa-oyJ4YZMKBoId-3ZLkIUFzC8kcU9zRGJpo" }
    
settings = Settings()
