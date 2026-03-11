from fastapi import Request
from src.models.userModel import User
from src.schemas.userSchema import UserSchema, UserEditSchema
from src.services.userService import UserService

class UserAdapter:

    def read_all_users_controller(self, request: Request):
        users = UserService().read_all_users(request.query_params)
        return {"erro": False, "data": users}

    def read_user_by_id_controller(self, request: Request):
        user = UserService().read_user_by_id(request.query_params)
        return {"erro": False, "data": user}

    def read_user_by_email_controller(self, request: Request):
        users = UserService().read_user_by_email(request.query_params)
        return {"erro": False, "data": users}

    def read_user_by_name_controller(self, request: Request):
        users = UserService().read_user_by_name(request.query_params)
        return {"erro": False, "data": users}

    def add_user_controller(self, schema: UserSchema):

        newUser = User(
            id=None, 
            name=schema.name, 
            email=schema.email, 
            password=schema.password, 
            card_id=None
        )

        new_user_id: int = UserService().add_user(new_user=newUser.model_dump())
        return {"erro": False, "message" : "user added sucessfully", "id": new_user_id}

    def update_user_controller(self, id: int, user_to_update: UserEditSchema):
        edited_id = UserService().update_user(id, user_to_update.model_dump())
        return {"erro": False, "message" : "user edited sucessfully", "id": edited_id}

    def kill_yourself_controller(self, id: int):
    # def delete_user_controller(self, id: int):
        # UserService().delete_user(id=id)
        deleted_id = UserService().kill_yourself(id=id)
        return {"erro": False, "message" : "user deleted sucessfully", "id": deleted_id}
