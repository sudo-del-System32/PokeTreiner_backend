
from fastapi import HTTPException, status, Depends
from src import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, email_validator, REFRESH_TOKEN_SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM_TO_HASH
from datetime import timedelta
from src.services.userService import UserService
from src.services import SuperService 
from src.services.authService import create_tolkien 

from src.controllers import form_auth_dependency

from jose import jwt, ExpiredSignatureError, JWTError

class AuthAdapter:

    def login(self, data: form_auth_dependency):
        
        if not email_validator(data.username):
            raise ValueError("invalid email format.")

        user = UserService().get_user_by_email(data.username.lower())
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect."
            )
        
        if data.password != user.get("password"): 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is incorrect."
            )

        access_tolkien = create_tolkien(
            user_id=str(user.get("id")),  
            expire_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
            SECRET=SECRET_KEY
        ) 

        refresh_tolkien = create_tolkien(
            user_id=str(user.get("id")),  
            expire_time=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), 
            SECRET=REFRESH_TOKEN_SECRET_KEY
        ) 

        return {
            "access_token": access_tolkien,
            "refresh_token": refresh_tolkien,
            "token_type": "bearer"
            }

    def refresh_token(self, refresh_token: str):
        payload = self.decode_refresh(refresh_token=refresh_token)
        
        user_id = payload.get("id", None)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Key does not have an id."
                )
        
        user = UserService().get_user_by_id(user_id)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found."
            )
        
        new_access_tolkien = create_tolkien(
            user_id=str(user.get("id")),  
            expire_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
            SECRET=SECRET_KEY
        ) 

        new_refresh_tolkien = create_tolkien(
            user_id=str(user.get("id")),  
            expire_time=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), 
            SECRET=REFRESH_TOKEN_SECRET_KEY
        ) 

        return {
            "access_token": new_access_tolkien,
            "refresh_token": new_refresh_tolkien,
            "token_type": "bearer"
            }

    def decode_refresh(self, refresh_token: str):
        try:
            payload = jwt.decode(
                token=refresh_token, 
                key=REFRESH_TOKEN_SECRET_KEY, 
                algorithms=ALGORITHM_TO_HASH
            )

            return payload
        
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Expired refresh token."
                )
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"Invalid refresh token."
                )
