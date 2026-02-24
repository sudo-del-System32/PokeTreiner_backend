from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[int]
    nome: str
    idade: int

    nomeDeUsuario: str
    email: str
    senha: str

    def __init__(self, id, nome, idade, nomeDeUsuario, email, senha):

        super().__init__(
            id=id,
            nome=nome,
            idade=idade,
            nomeDeUsuario=nomeDeUsuario,
            email=email,
            senha=senha,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "nomeDeUsuario": self.nomeDeUsuario,
            "email": self.email,
            "senha": self.senha,
        }

    def __repr__(self):
        return f"<User {self.id} {self.nome} {self.idade} {self.nomeDeUsuario} {self.email} {self.senha}>"
