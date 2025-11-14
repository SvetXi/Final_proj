class TestData:
    # API Test Data
    SEARCH_PHRASES = {
        "cyrillic": "книга",
        "latin": "Book", 
        "special_chars": "!@#$%",
        "numbers": "123",
        "existing_product": "Сияние"  
    }
    
    # UI Test Data 
    VALID_PHONE = "+79111111111"  
    SMS_CODE = "000000" 
    SEARCH_QUERY = "книга" 
    AUTHOR_FILTER = "Достоевский" 
    
    # Expected Messages
    ERROR_MESSAGES = {
        "invalid_phrase": "Недопустимая поисковая фраза",
        "empty_phrase": "Значение не должно быть пустым",
        "unauthorized": "Authorization обязательное поле"
    }
    
    # URLs 
    AUTH_URL = "/login"
    SEARCH_URL = "/search"
    CART_URL = "/cart"
    MAIN_URL = "/"

test_data = TestData()