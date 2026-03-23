from fastapi import Request

from fastapi import Request, HTTPException, status, Depends
from src import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, email_validator
from datetime import timedelta
from src.services.userService import UserService
from src.services import SuperService 
from src.models.userModel import User  
from src.services.authService import create_tolkien 

from src.controllers import form_auth_dependency

class AuthAdapter:

    def login(self, data: form_auth_dependency):
        
        if not email_validator(data.username):
            raise ValueError("invalid email.")

        user = SuperService(UserService().connect).find(column_query="id, password", table="users", collumns=["email"], data=[data.username,])
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="email or password is incorrect"
            )
        
        user = {
            "id": user[0][0],
            "password": user[0][1] # type: ignore
        }

        if data.password != user.get("password"): 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email or password is incorrect"
            )

        code_jwt = create_tolkien(
            user_id=user.get("id"),  # type: ignore
            expire_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
            SECRET=SECRET_KEY
        ) 
        return {
            "access_token": code_jwt,
            "token_type": "bearer"
            }
