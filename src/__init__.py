from pydantic import AfterValidator
from typing import Annotated
from passlib.context import CryptContext
from re import match


def email_validator(email: str):
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not match(EMAIL_PATTERN, email):
        raise ValueError(
            "Invalid email format."
        )
    
    validated_email = email.lower() 
    return validated_email

Email = Annotated[str, AfterValidator(email_validator)]

ALGORITHM_TO_HASH = "HS512"
SECRET_KEY = "0819649a7e879be85b2d0e54322fd3c8328d249c10fc32a0945033c051c75796"
REFRESH_TOKEN_SECRET_KEY = "ffd4bce97d799a1927b119b009218295d20146a689af91b239f7e63d6b84fe40"
SALT_HASH_PASSWORD = "LXaui9F6n5JL1Mcz" # Para salgar a senha
# Made using "openssl rand -hex 32" 

REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_MINUTES = 15



bcrypt_that_works = CryptContext(    
    deprecated="auto",
    schemes=["sha512_crypt"],
    sha512_crypt__default_rounds=5000 # Padrao linux
)