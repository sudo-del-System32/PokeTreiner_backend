from fastapi import APIRouter, Request
from src.schemas.userSchema import UserSchema, UserEditSchema
from src.adapters.userAdapter import UserAdapter

router = APIRouter(prefix="/user") 


@router.get("/")
async def read_all_users(request: Request, page: int=1, rows_per_page: int=10):
    # djeizu: dict = await request.json() # await utiliza junto de async function
    # if djeizu.get("email") is None:
    return UserAdapter().read_all_users_controller(request=request)

@router.get("/search/id/{id}")
async def read_user_by_id(request: Request, user_id: int):
    return UserAdapter().read_user_by_id_controller(request=request)

@router.get("/search/email/{email}")
async def read_user_by_email(request: Request, user_email: str, page: int=1, rows_per_page: int=10):
    return UserAdapter().read_user_by_email_controller(request=request)

@router.get("/search/name/{name}")
async def read_user_by_name(request: Request, user_name: str, page: int=1, rows_per_page: int=10):
    return UserAdapter().read_user_by_name_controller(request=request)

@router.post("/")
async def add_user(schema: UserSchema):
    return UserAdapter().add_user_controller(schema)

@router.put("/")
async def update_user(id: int, user_to_update: UserEditSchema):
    return UserAdapter().update_user_controller(id, user_to_update)


@router.delete("/")
async def kill_yourself(id: int):
# async def delete_user(id: int):
    # return UserAdapter().delete_user_controller(id=id)
    return UserAdapter().kill_yourself_controller(id=id)