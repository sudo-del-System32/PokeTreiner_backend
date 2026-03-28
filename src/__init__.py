from re import match

def email_validator(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return match(email_pattern, email)

ALGORITHM_TO_HASH = "HS512"
SECRET_KEY = "0819649a7e879be85b2d0e54322fd3c8328d249c10fc32a0945033c051c75796"
REFRESH_TOKEN_SECRET_KEY = "ffd4bce97d799a1927b119b009218295d20146a689af91b239f7e63d6b84fe40"
# Made using "openssl rand -hex 32" 

REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_MINUTES = 15