import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    BASE_API_URL = "https://web-agr.chitai-gorod.ru/web/api/v2"
    API_TIMEOUT = 10
    
    # UI Settings
    BASE_UI_URL = "https://www.chitai-gorod.ru"
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    
    # Test Data
    CUSTOMER_CITY_ID = 213
    AB_TEST_GROUP = 1

settings = Settings()