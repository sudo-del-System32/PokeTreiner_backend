from pydantic import BaseModel, model_validator, Field
from typing import Optional
from src import Email

from re import match

class UserAddSchema(BaseModel):
    name: str = Field(min_length=1, max_length=25)
    email: Email = Field(min_length=1, max_length=320)
    password: str = Field(min_length=4, max_length=25)


class UserEditSchema(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=25, default=None)
    email: Optional[Email] = Field(min_length=1, max_length=320, default=None)
    password: Optional[str] = Field(min_length=1, max_length=25, default=None)
