from fastapi import APIRouter, Request
from src.schemas.userSchema import UserAddSchema, UserEditSchema
from src.adapters.userAdapter import UserAdapter
from src.controllers import user_dependency

router = APIRouter(prefix="/user", tags=["user"]) 


@router.get("/all")
async def read_all_users(curr_user: user_dependency, request: Request, page: int=1, rows_per_page: int=10):
    return UserAdapter().read_all_users_controller(request=request)

@router.get("/search/{user_id}")
async def read_user_by_id(user: user_dependency, request: Request, user_id: int):
    return UserAdapter().read_user_by_id_controller(request=request)

@router.get("/search/email/{user_email}")
async def read_user_by_email(user: user_dependency, request: Request, user_email: str, page: int=1, rows_per_page: int=10):
    return UserAdapter().read_user_by_email_controller(request=request)

@router.get("/search/name/{user_name}")
async def read_user_by_name(user: user_dependency, request: Request, user_name: str, page: int=1, rows_per_page: int=10):
    return UserAdapter().read_user_by_name_controller(request=request)

@router.post("/register")
async def add_user(schema: UserAddSchema):
    return UserAdapter().add_user_controller(schema)

@router.put("/edit/{id}")
async def update_user(user: user_dependency, id: int, user_to_update: UserEditSchema):
    return UserAdapter().update_user_controller(user, id, user_to_update)


@router.delete("/delete/{id}")
async def kill_yourself(user: user_dependency, id: int):
    return UserAdapter().kill_yourself_controller(user, id=id)