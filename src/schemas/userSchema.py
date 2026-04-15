from pydantic import BaseModel, model_validator, Field
from typing import Optional
from src import Email

from re import match
PASSWORD_REGEX = r"^[a-zA-Z0-9._%+-!@#$%^&*]$" 
# Verificar quais credenciais o cadu pediu na senha no front

class UserAddSchema(BaseModel):
    name: str = Field(min_length=1, max_length=25)
    email: Email = Field(min_length=1, max_length=320)
    password: str = Field(min_length=4, max_length=25)

    @model_validator(mode="after")
    def password_validato(self):
        if match(PASSWORD_REGEX, self.password) is None:
            raise ValueError("Password must have only contain letters, numbers and speacial characters")
    
        return self


class UserEditSchema(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=25, default=None)
    email: Optional[Email] = Field(min_length=1, max_length=320, default=None)
    password: Optional[str] = Field(min_length=1, max_length=25, default=None)

    @model_validator(mode="after")
    def password_validato(self):
        if self.password is None:
            return self
        
        if match(PASSWORD_REGEX, self.password) is None:
            raise ValueError("Password must have only contain letters, numbers and speacial characters")
    
        return self
    

# Excluir dps
class UserReturnSchema(BaseModel):
    id: int
    name: str
    email: str
    
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
    
