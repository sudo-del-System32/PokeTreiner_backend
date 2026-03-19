from fastapi import Request

from fastapi import Request, HTTPException, status
from src import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from src.services.userService import UserService
from src.services.authService import create_tolkien 




class AuthAdapter:

    def login(self, request: Request):
        
        user = UserService().read_user_by_email({"email": request.query_params.get("email")}, request.query_params)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="email or password is incorrect"
            )
        
        if request.query_params.get("password") != user.password: # type: ignore
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email or password is incorrect"
            )

        code_jwt = create_tolkien(
            user_id=user.id,  # type: ignore
            expire_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
            SECRET=SECRET_KEY
        ) 
        return {
            "access _token": code_jwt,
            "token_type": "Bearer"
            }
