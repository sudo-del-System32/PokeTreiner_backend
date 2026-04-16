from typing import Optional
from src import Model
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(25), nullable=False)
    
    def __init__(
        self, 
        name: str,
        email: str,
        password: str
        ):
        self.name = name
        self.email = email
        self.password = password

    # Same as __dict__ but manually made
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }

    # Representation: how its printed when printed 
    def __repr__(self) -> str:
        return f"<User {self.id}, {self.name}, {self.email}, {self.password}>"
    