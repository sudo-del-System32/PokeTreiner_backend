import sqlite3 as sql
from src import database
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.services import SuperService
from src import SECRET_KEY, ALGORITHM_TO_HASH, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from jose import jwt, ExpiredSignatureError
from typing import Any
from src.services.userService import UserService

from src.adapters.authAdapter import AuthAdapter

router = APIRouter(prefix="/auth") 

@router.post("/login")
async def login(request: Request, email: str, password: str):
    content = AuthAdapter().login(request=request)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)

@router.post("/me")
def me(request: Request, tolkien: str):
    
    if not tolkien:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="token doesn't exist")

    try:
        payload = jwt.decode(token=tolkien, key=SECRET_KEY, algorithms=ALGORITHM_TO_HASH)
        
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user is not authorized to do this action")
        
        user = UserService().read_user_by_id({"user_id": user_id})

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        
        return user
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="expired token")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"error in user authentication: {e}")
    