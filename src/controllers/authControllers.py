from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src import SECRET_KEY, ALGORITHM_TO_HASH
from jose import jwt, ExpiredSignatureError
from src.services.userService import UserService
from src.adapters.authAdapter import AuthAdapter
from src.controllers import user_dependency

router = APIRouter(prefix="/auth") 

@router.post("/login")
async def login(request: Request, email: str, password: str):
    content = AuthAdapter().login(request=request)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)

@router.post("/me")
def me(request: Request, user: user_dependency):
    
    return UserService().read_user_by_id({"user_id": user.get("id")})
