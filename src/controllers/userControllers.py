from fastapi import APIRouter, Request
from src.classes import User, DataBank
from src.schemas.userSchema import UserSchema
from src.services.userService import UserService

bd = DataBank("databases/dataBank.db")

router = APIRouter(prefix="/user") 


@router.get("/")
async def read_all_users(request: Request):
    # djeizu: dict = await request.json() # await utiliza junto de async function
    # if djeizu.get("email") is None:
    return bd.user_list()


@router.get("/{id}")
def read_user(id):
    return bd.search("id", id)


@router.get("/search")
def read_user(campo: str, dado):
    return bd.search(campo, dado)


@router.post("/")
def add_user(user: User):
    service = UserService()
    service.add_user(new_user=user)

@router.delete("/")
def delete_user(id: int):
    try:
        bd.delete(id)
        return {"mensagem": "Usuario deletado"}

    except Exception as e:
        return {"mensagem": f"Erro no apagamento: {e}"}
