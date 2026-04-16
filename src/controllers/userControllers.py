from fastapi import APIRouter, Request
from src.schemas.userSchema import UserAddSchema, UserEditSchema
from src.adapters.userAdapter import UserAdapter
from src.controllers import user_dependency

router = APIRouter(prefix="/user", tags=["user"]) 


@router.get("/all")
async def read_all_users(curr_user: user_dependency, request: Request, page: int=1, rows_per_page: int=10):
    return UserAdapter().get_all_users_controller(request=request)

@router.get("/search/{user_id}")
async def read_user_by_id(curr_user: user_dependency, user_id: int):
    return UserAdapter().get_user_by_id_controller(user_id)

@router.get("/search/email/{email}")
async def read_user_by_email(curr_user: user_dependency, email: str, request: Request, page: int=1, rows_per_page: int=10):
    return UserAdapter().get_user_by_email_controller(email, request)

@router.get("/search/name/{name}")
async def read_user_by_name(curr_user: user_dependency, name: str, request: Request, page: int=1, rows_per_page: int=10):
    return UserAdapter().get_user_by_name_controller(name, request)

@router.post("/register")
async def add_user(schema: UserAddSchema):
    return UserAdapter().add_user_controller(schema)

@router.put("/edit/{id}")
async def update_user(curr_user: user_dependency, user_id: int, user_to_update: UserEditSchema):
    return UserAdapter().update_user_controller(curr_user, user_id, user_to_update)


@router.delete("/delete/{id}")
async def kill_yourself(curr_user: user_dependency, user_id: int):
    return UserAdapter().kill_yourself_controller(curr_user, user_id)
