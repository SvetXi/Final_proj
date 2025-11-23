import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    BASE_API_URL = "https://web-agr.chitai-gorod.ru/web/api/v2"
    API_TIMEOUT = 30
    
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
    API_TOKEN = "your_token_here"

    
settings = Settings()

