import sqlite3 as sql

from typing import List, Optional

from src.classes import User


class DataBank:
    def __init__(self, dataBankName):
        try:
            self.dataBankName = dataBankName
            self.connect = sql.connect(self.dataBankName)
            self.cursor = self.connect.cursor()
            self.start()
            self.connect.close()

        except Exception as e:
            print("Error:", e)

    def start_connection(self):
        self.connect = sql.connect(self.dataBankName)
        self.cursor = self.connect.cursor()

    def start(self):

        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        nome TEXT,
                        idade INTEGER,
                                
                        nomeDeUsuario TEXT UNIQUE,
                        email TEXT UNIQUE,
                        senha TEXT
                )
            """)

            self.connect.commit()

        except Exception as e:
            print("Error:", e)
            return None

    def add_user(self, new_user: User):

        self.start_connection()

        try:
            info: tuple = tuple(new_user.__dict__.values())
            self.cursor.execute(
                """INSERT INTO users (id , nome, idade, nomeDeUsuario, email, senha) VALUES (?, ?, ?, ?, ?, ?)""",
                (info),
            )
            self.connect.commit()

            self.connect.close()
            return True

        except Exception as e:
            print("Error:", e)

            self.connect.close()
            return False

    def search(self, campo: str, info: str):

        self.start_connection()

        try:
            cursor = self.cursor.execute(
                f"SELECT * FROM users WHERE {campo} = ?", (info,)
            )

            found_users: List[User] = []

            for user in cursor.fetchall():
                id, nome, idade, nomeDeUsuario, email, senha = user
                found_users.append(User(id, nome, idade, nomeDeUsuario, email, senha))

            self.connect.close()
            return found_users

        except Exception as e:
            print("Error:", e)

            self.connect.close()
            return None

    def user_list(self):

        self.start_connection()

        try:
            cursor = self.cursor.execute("SELECT * FROM users")

            list_of_users: List[User] = []

            for user in cursor.fetchall():
                id, nome, idade, nomeDeUsuario, email, senha = user
                list_of_users.append(User(id, nome, idade, nomeDeUsuario, email, senha))

            self.connect.close()
            return list_of_users

        except Exception as e:
            print("Error:", e)

            self.connect.close()
            return None

    def update(self, id: int, campo: str, newInfo: str):

        self.start_connection()

        try:
            self.cursor.execute(
                f"""UPDATE users SET {campo} = ? WHERE id = ? """, (newInfo, id)
            )
            self.connect.commit()

            self.connect.close()
            return True

        except Exception as e:
            print("Error:", e)

            self.connect.close()
            return False

    def delete(self, id: int):

        self.start_connection()

        try:
            self.cursor.execute(f"""DELETE FROM users WHERE id = ?""", (id,))
            self.connect.commit()

            self.connect.close()
            return True

        except Exception as e:
            print("Error:", e)

            self.connect.close()
            return False
