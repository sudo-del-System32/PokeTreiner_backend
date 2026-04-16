from fastapi import HTTPException, Request, status
from src.models.userModel import User
from src.schemas.userSchema import UserAddSchema, UserEditSchema
from src.services.userService import UserService
from src.controllers import user_dependency
from src.adapters import get_pagination
from src import bcrypt_that_works, SALT_HASH_PASSWORD

class UserAdapter:

    def get_all_users_controller(self, request: Request):

        users, total = UserService().get_all_users(request.query_params)

        for user in users:
            if user is not None:
                user.update({'password': 'secret'})

        output = get_pagination(users, total)
    
        output.update({'error': True})
        
        return output

    def get_user_by_id_controller(self, user_id: int):

        user = UserService().get_user_by_id(user_id)
        
        if user is None: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User with this id was not found."
            )
            
        user.update({'password': 'secret'})
        
        return {
                "data": user,
                "error": False 
            }

    def get_user_by_email_controller(self, email: str, request: Request):
        
        users, total = UserService().get_user_by_similarity_to_email(email, request.query_params)

        for user in users:
            if user is not None:
                user.update({'password': 'secret'})
    
        output = get_pagination(users, total)
    
        output.update({'error': True})
        
        return output

    def get_user_by_name_controller(self, name: str, request: Request):

        users, total = UserService().get_user_by_name(name, request.query_params)

        for user in users:
            if user is not None:
                user.update({'password': 'secret'})

        output = get_pagination(users, total)
    
        output.update({'error': True})
        
        return output

    def add_user_controller(self, schema: UserAddSchema):
        schema.password = bcrypt_that_works.hash(secret=schema.password, salt=SALT_HASH_PASSWORD)
        
        user = UserService().get_user_by_email(schema.email)
        
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email is already in use."
            )

        # Verify if its converted in adapter or in service
        newUser = User(
            name=schema.name, 
            email=schema.email, 
            password=schema.password, 
        )

        new_user_dict = UserService().add_user(newUser)
        
        return {
                "message" : "user added sucessfully",
                "data": new_user_dict,
                "error": False
            }

    def update_user_controller(self, curr_user: user_dependency, user_id: int, user_to_update: UserEditSchema):
        
        if curr_user.get("id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User can't do this action for another user."
            )


        if user_to_update.email is not None:
            user_found = UserService().get_user_by_email(user_to_update.email) 

            if user_found is not None and user_found.get("id") != user_id: 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Email is already in use."
                )

        if user_to_update.password is not None:
            user_to_update.password = bcrypt_that_works.hash(secret=user_to_update.password, salt=SALT_HASH_PASSWORD)

        user_dict = UserService().update_user(user_id, user_to_update)
        
        return {
                "message" : "user edited sucessfully",
                "data": user_dict,
                "error": False
            }

    def kill_yourself_controller(self, curr_user: user_dependency, user_id: int):
        
        if curr_user.get("id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User can't do this action for another user."
            )

        user_dict = UserService().kill_yourself(user_id) 
        return {
                "message" : "user deleted sucessfully", 
                "data": user_dict,
                "error": False
            }
