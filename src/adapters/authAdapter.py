
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
            raise ValueError("invalid email.")

        user = SuperService(UserService().connect).find(
            column_query="id, password",
            table="users", 
            collumns=["email"], 
            data=[data.username,]
            )
        
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

        access_tolkien = create_tolkien(
            user_id=user.get("id"),  # type: ignore
            expire_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
            SECRET=SECRET_KEY
        ) 

        refresh_tolkien = create_tolkien(
            user_id=user.get("id"),  # type: ignore
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
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="key does not have id"
                )
        
        user = SuperService(UserService().connect).find(
            column_query="id",
            table="users", 
            collumns=["id"], 
            data=[user_id,]
            )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user not found"
                )
        user = { "id": user[0][0]}

        new_access_tolkien = create_tolkien(
            user_id=user.get("id"),  # type: ignore
            expire_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
            SECRET=SECRET_KEY
        ) 

        new_refresh_tolkien = create_tolkien(
            user_id=user.get("id"),  # type: ignore
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
                detail="expired refresh token"
                )
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"invalid refresh token"
                )
