from pydantic import BaseModel, model_validator, Field
from typing import Optional
from src import Email

class UserAddSchema(BaseModel):
    name: str = Field(min_length=1, max_length=25)
    email: Email = Field(min_length=1, max_length=320)
    password: str = Field(min_length=4, max_length=25)

    # @model_validator(mode="after")
    # def check_email(self):
    #     if not email_validator(self.email):
    #         raise ValueError("invalid email")

    #     return self

class UserEditSchema(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=25, default=None)
    email: Optional[Email] = Field(min_length=1, max_length=320, default=None)
    password: Optional[str] = Field(min_length=1, max_length=25, default=None)

    # @model_validator(mode="after")
    # def check_email(self):
    #     if self.email is None:
    #         return self
        
    #     if not email_validator(self.email):
    #         raise ValueError("invalid email")
        
    #     return self
    

# Excluir dps
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
    
