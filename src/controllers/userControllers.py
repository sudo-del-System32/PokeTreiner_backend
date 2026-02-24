from fastapi import FastAPI, APIRouter
from src.classes import User, DataBank


bd = DataBank("databases/dataBank.db")

app = FastAPI()

router = APIRouter(prefix="/user")


@app.get("/")
def read_all_users():
    return bd.user_list()


@app.get("/{id}")
def read_user(id):
    return bd.search("id", id)


@app.get("/search")
def read_user(campo: str, dado):
    return bd.search(campo, dado)


@app.post("/")
def add_user(user: User):
    try:
        bd.add_user(user)
        return {"mensagem": "Usuario cadastrado"}

    except Exception as e:
        return {"mensagem": f"Erro no cadastro: {e}"}


@app.delete("/")
def delete_user(id: int):
    try:
        bd.delete(id)
        return {"mensagem": "Usuario deletado"}

    except Exception as e:
        return {"mensagem": f"Erro no apagamento: {e}"}
