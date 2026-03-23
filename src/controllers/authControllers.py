from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from src.services.userService import UserService
from src.controllers import user_dependency
from src.adapters.authAdapter import AuthAdapter, form_auth_dependency


router = APIRouter(prefix="/auth", tags=["auth"]) 


@router.post("/login")
async def login(data: form_auth_dependency):
    content = AuthAdapter().login(data)
    return content#JSONResponse(status_code=status.HTTP_201_CREATED, content=content)

@router.post("/me")
def me(request: Request, user: user_dependency):
    return user
    # return UserService().read_user_by_id({"user_id": user.get("id")}) o user_dependency ja acha o usuario
