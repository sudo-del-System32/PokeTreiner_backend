from re import match

def email_validator(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return match(email_pattern, email)

ALGORITHM_TO_HASH = "HS512"
SECRET_KEY = "0819649a7e879be85b2d0e54322fd3c8328d249c10fc32a0945033c051c75796"


ACCESS_TOKEN_EXPIRE_MINUTES = 15