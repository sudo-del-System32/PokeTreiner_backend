import sqlite3 as sql
from src import database
from src.models.userModel import User # Talvez não



class UserService:

    def __init__(self):
        self.connect = sql.connect("databases/dataBank.db")
        self.cursor = self.connect.cursor()

    def read_all_users(self):
        cursor = self.cursor.execute("""
                SELECT * FROM users
            """
        )

        found_users: list[User] = []

        for user in cursor.fetchall():
            user = list(user)
            user[3] = "1234"
            found_users.append(User(
                id=user[0],
                name=user[1],
                email=user[2],
                password=user[3],
                card_id=user[4]
                ))
        
        return found_users

    def read_user(self, id): 

        cursor = self.cursor.execute("""
                SELECT * 
                FROM users
                WHERE
            """
        )


    def add_user(self, new_user : User):
        data = tuple(new_user.__dict__.values())
        
        self.cursor.execute("""
                INSERT INTO users
                (id, name, email, password, card_id)
                VALUES
                (?, ?, ?, ?, ?)
            """,
            (data)
        )
        self.connect.commit()
        self.connect.close()

