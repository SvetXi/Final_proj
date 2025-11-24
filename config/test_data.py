class TestData:
    # API Test Data
    SEARCH_PHRASES = {
        "cyrillic": "книга",
        "latin": "book", 
        "special_chars": "!@#$%",
        "cyrillic plus numbers": "книга 12",
        "numbers": "книга 12"
    }
    
    # UI Test Data
    VALID_PHONE = "+79111111111"
    SEARCH_QUERY = "книга"
    AUTHOR_FILTER = "книги"

test_data = TestData()

