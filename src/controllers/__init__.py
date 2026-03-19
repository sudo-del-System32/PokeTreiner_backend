from jose import jwt
from typing import Any, Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# def get_current_user(token: token):
#     pass


# user_dependency = Annotated[dict[str, Any], Depends(get_current_user)]
