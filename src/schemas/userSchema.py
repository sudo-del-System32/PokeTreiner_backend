from pydantic import BaseModel, model_validator
from typing import Optional
from src import email_validator

class UserSchema(BaseModel):
    name: str
    email: str
    password: str

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

class UserEditSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @model_validator(mode="after")
    def check_name(self):
        if not self.name:
            return self
        
        if len(self.name) < 1:
            raise ValueError("User name can not be empty")
        return self
    
    @model_validator(mode="after")
    def check_email(self):
        if not self.email:
            return self
        
        if not email_validator(self.email):
            raise ValueError("invalid email")
        
        if len(self.email) < 1:
            raise ValueError("User email can not be empty")
        return self
    
    @model_validator(mode="after")
    def check_password(self):
        if not self.password:
            return self

        if len(self.password) < 4:
            raise ValueError("User password needs to be bigger than 4 digits")
        return self

class UserReturnSchema(BaseModel):
    id: int
    name: str
    email: str
    card_id: Optional[int]
    
    @model_validator(mode="after")
    def check_name(self):
        if len(self.name) < 1:
            raise ValueError("User name can not be empty")
        return self
    
    @model_validator(mode="after")
    def check_email(self):
        if len(self.email) < 1:
            raise ValueError("User email can not be empty")
        return self
    
