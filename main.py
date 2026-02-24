from fastapi import FastAPI
from src.classes import User, DataBank

bd = DataBank("databases/dataBank.db")

app = FastAPI()


@app.get("/users")
def read_all_users():
    return bd.user_list()


@app.get("/users/search/{id}")
def read_user(id):
    return bd.search("id", id)


@app.get("/users/search")
def read_user(campo : str, dado):
    return bd.search(campo, dado)


@app.post("/users")
def add_user(user : User):
    try:
        bd.add_user(user)
        return {'mensagem' : 'Usuario cadastrado'}
    
    except Exception as e:
        return {'mensagem' : f'Erro no cadastro: {e}'}


@app.delete("/users")
def delete_user(user : User):
    try:
        bd.delete(user.id)
        return {'mensagem' : 'Usuario deletado'}
    
    except Exception as e:
        return {'mensagem' : f'Erro no apagamento: {e}'}


@app.delete("/users/")
def delete_user(id : int):
    try:
        bd.delete(id)
        return {'mensagem' : 'Usuario deletado'}
    
    except Exception as e:
        return {'mensagem' : f'Erro no apagamento: {e}'}

