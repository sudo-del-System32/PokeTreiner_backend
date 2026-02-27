import sqlite3 as sql
from src import database
from src.models.userModel import User # Talvez não



class UserService:

    def __init__(self):
        self.connect = sql.connect("databases/dataBank.db")
        self.cursor = self.connect.cursor()


    def add_user(self, new_user : User):
        data = tuple(new_user.__dict__.values())
        
        self.cursor.execute("""
                INSERT INTO users
                (id, name, email, password)
                VALUES
                (?, ?, ?, ?)
            """,
            (data[0], data[1], data[2], data[3])
        )
        self.connect.commit()
        self.connect.close()

