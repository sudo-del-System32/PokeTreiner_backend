from typing import Any
from fastapi import HTTPException, status
from fastapi.datastructures import QueryParams
from src.models.userModel import User
from src.schemas.userSchema import UserEditSchema   
from . import SuperService

from sqlalchemy import Select, select, Insert, func, case

class UserService:

    def get_all_users(
            self, 
            query_params: QueryParams
        ) -> tuple[list[dict[str, Any] | None], int | None]:

        stmt = select(User)
        users, total = SuperService().get_all_with_pagination(
            stmt, 
            page=int(query_params.get("page", 1)), 
            rows_per_page=int(query_params.get("rows_per_page", 10))
        )

        user_list = [user.to_dict() for user in users] # Converts in list and the itens of the list in dicts

        return user_list, total

    def get_user_by_id(
            self, 
            user_id: int
        ) -> dict[str, Any] | None:

        user = SuperService().get_by_id(user_id, User)
        
        if user is None:
            return None
        
        return user.to_dict()

    def get_user_by_similarity_to_email(
            self,
            email: str,
            query_params: QueryParams
        ) -> tuple[list[dict[str, Any] | None], int | None]:

        # Ordenação de acordo com similaridade
        email_1 = f'{email}%'
        email_2 = f'%{email}%'
        
        case_clause = case(
            (User.email.like(email_1), 1),
            (User.email.like(email_2), 2),
            else_=3
        )

        stmt = (
            select(User)
            .filter(User.email.like(email_2))
            .order_by(case_clause, User.email.asc())
        )
        users, total = SuperService().get_all_with_pagination(
            stmt,
            page=int(query_params.get("page", 1)), 
            rows_per_page=int(query_params.get("rows_per_page", 10))
        )

        user_list = [user.to_dict() for user in users]

        return user_list, total
    
    def get_user_by_email(
            self, 
            email: str
        ) -> dict[str, Any] | None:

        stmt = select(User).filter_by(email=email)
        user = SuperService().get(stmt)

        if user is None:
            return None

        return user.to_dict()
 
    
    def get_user_by_name(
            self,            
            name: str,
            query_params: QueryParams
        ) -> tuple[list[dict[str, Any] | None], int | None]:

        # Ordenação de acordo com similaridade
        name_1 = f'{name}%'
        name_2 = f'%{name}%'
        
        case_clause = case(
            (User.name.like(name_1), 1),
            (User.name.like(name_2), 2),
            else_=3
        )

        stmt = (
            select(User)
            .filter(User.name.like(name_2))
            .order_by(case_clause, User.name.asc())
        )
        users, total = SuperService().get_all_with_pagination(
            stmt,
            page=int(query_params.get("page", 1)),
            rows_per_page=int(query_params.get("rows_per_page", 10)) 
        )

        user_list = [user.to_dict() for user in users]

        return user_list, total

    def add_user(
            self, 
            new_user: User
        ) -> dict[str, Any]:

        user = SuperService().add(new_user)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="New user was not subscribed, try again.")
        
        return user.to_dict()

    def update_user(
            self, 
            user_id: int, 
            user_to_update: UserEditSchema
        ) -> dict[str, Any] | None:

        user = SuperService().edit_by_id(user_id, User, user_to_update)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        return user.to_dict()

    def kill_yourself(self, user_id: int):

        user = SuperService().delete_by_id(user_id, User)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        return user.to_dict()
