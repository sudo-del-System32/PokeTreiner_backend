from pydantic import BaseModel, model_validator
from typing import Optional
from src import email_validator

class User(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    card_id: Optional[int]
    
    @model_validator(mode="after")
    def check_name(self):
        if len(self.name) < 1:
            raise ValueError("User name can not be empty")
        return self
    
    @model_validator(mode="after")
    def check_email(self):
        if not email_validator(self.email):
            raise ValueError("invalid email")

        if len(self.email) < 1:
            raise ValueError("User email can not be empty")
        return self
    
    @model_validator(mode="after")
    def check_password(self):
        if len(self.password) < 4:
            raise ValueError("User password needs to be bigger than 4 digits")
        return self

