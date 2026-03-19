import sqlite3 as sql
from typing import Any
from fastapi import HTTPException, status
from fastapi.datastructures import QueryParams
from src import database
from src.models.userModel import User
from src.schemas.userSchema import UserReturnSchema, UserSchema, UserEditSchema
from . import SuperService, pagination, pagination_like

class UserService:

    def __init__(self):
        self.connect = sql.connect("databases/dataBank.db")
        self.cursor = self.connect.cursor()

    def read_all_users(self, query_params: QueryParams):

        users = SuperService(self.connect).find(column_query="id, name, email, card_id", table="users", page=int(query_params.get("page", 1)), rows_per_page=int(query_params.get("rows_per_page", 10)))

        found_users: list[UserReturnSchema] = []

        for user in users: 
            id, name, email, card_id = user
            found_users.append(UserReturnSchema(
                id=id,
                name=name,
                email=email,
                card_id=card_id
                ))
        
        output = pagination(connection=self.connect, table="users", itens=found_users, page=int(query_params.get("page", 1)), rows_per_page=int(query_params.get("rows_per_page", 10)))

        self.connect.close()
        return output

    def read_user_by_id(self, path_params: dict[str, Any]):

        id = path_params.get('user_id')
        user_found = SuperService(self.connect).find(column_query="id, name, email, card_id", table="users", collumns=["id"], data=[id,])
        
        if not user_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        user_found = user_found[0]
            
        id, name, email, card_id = user_found
        found_users = UserReturnSchema(
            id=id,
            name=name,
            email=email,
            card_id=card_id
        )

        self.connect.close()
        return found_users

    def read_user_by_email_likewise(self, path_params: dict[str, Any], query_params: QueryParams):

        user_found = SuperService(self.connect).find_like(column_query="id, name, email, card_id", table="users", column="email", target=str(path_params.get("user_email")), page=int(query_params.get("page", 1)), rows_per_page=int(query_params.get("rows_per_page", 10)))
        
        if not user_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        found_users: list[UserReturnSchema] = []

        for user in user_found:
            id, name, email, card_id = user
            found_users.append(UserReturnSchema(
                id=id,
                name=name,
                email=email,
                card_id=card_id
            ))

        output = pagination(connection=self.connect, table="users", query=f"WHERE email LIKE '%{path_params.get("user_email")}%' ", itens=found_users, page=int(query_params.get("page", 1)), rows_per_page=int(query_params.get("rows_per_page", 10)))

        self.connect.close()
        return output
    
    def read_user_by_email(self, query_params: QueryParams):

        user_found = SuperService(self.connect).find(column_query="id, name, email, password", table="users", collumns=["email"], data=[query_params.get("email"),])
        
        if not user_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        user = user_found[0]

        id, name, email, password = user
        user = User(
            id=id,
            name=name,
            email=email,
            password=password,
            card_id=None
        )

        self.connect.close()
        return user
 
    
    def read_user_by_name(self, path_params: dict[str, Any], query_params: QueryParams):

        user_found = SuperService(self.connect).find_like(column_query="id, name, email, card_id", table="users", column="name", target=str(path_params.get("user_name")), page=int(query_params.get("page", 1)), rows_per_page=int(query_params.get("rows_per_page", 10)))

        if not user_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        found_users: list[UserReturnSchema] = []

        for user in user_found:
            id, name, email, card_id = user
            found_users.append(UserReturnSchema(
                id=id,
                name=name,
                email=email,
                card_id=card_id
            ))
        
        output = pagination(connection=self.connect, table="users", query=f"WHERE name LIKE '%{path_params.get("user_name")}%' ", itens=found_users, page=int(query_params.get("page", 1)), rows_per_page=int(query_params.get("rows_per_page", 10)))

        self.connect.close()
        return output

    def add_user(self, new_user: dict[str, Any]):

        user_found = SuperService(self.connect).find(column_query="email", table="users", collumns=["email"], data=[new_user.get("email"),])
        if user_found:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is already in use")

        SuperService(self.connect).add(table="users", item_to_add=new_user)

        user = SuperService(self.connect).find(column_query="id", table="users", collumns=["email"], data=[new_user.get("email"),])
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="new user was not found in bank")
        
        self.connect.close()
        return user[0][0]

    def update_user(self, id: int, user_to_update: dict[str, Any]):

        user_found = SuperService(self.connect).find(column_query="id", table="users", collumns=["id"], data=[id,])
        if not user_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        
        if user_to_update.get("email"):
            user_found = SuperService(self.connect).find(column_query="id", table="users", collumns=["email"], data=[user_to_update.get("email"),])

            if user_found and user_found[0][0] != id: 
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is already in use")

        SuperService(self.connect).edit(table="users", item_to_update=user_to_update, query=f"WHERE id = '{id}'; ")

        self.connect.close()
        return id

    def kill_yourself(self, id: int):
    # def delete_user(self, id: int):

        user_found = SuperService(self.connect).find(column_query="id", table="users", collumns=["id"], data=[id,])
        if not user_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        SuperService(self.connect).delete(table="users", query=f"WHERE id = '{id}'")
        
        user_found = SuperService(self.connect).find(column_query="id", table="users", collumns=["id"], data=[id,])
        if user_found:
            raise HTTPException(status_code=status.WS_1013_TRY_AGAIN_LATER, detail="user was not deleted correctly")

        self.connect.close()
        return id
