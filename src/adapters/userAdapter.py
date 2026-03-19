from fastapi import HTTPException, Request, status
from src.models.userModel import User
from src.schemas.userSchema import UserSchema, UserEditSchema
from src.services.userService import UserService
from src.controllers import user_dependency


class UserAdapter:

    def read_all_users_controller(self, request: Request):
        users = UserService().read_all_users(request.query_params)
        return {"error": False, "data": users}

    def read_user_by_id_controller(self, request: Request):
        user = UserService().read_user_by_id(request.path_params)
        return {"error": False, "data": user}

    def read_user_by_email_controller(self, request: Request):
        users = UserService().read_user_by_email_likewise(request.path_params, request.query_params)
        return {"error": False, "data": users}

    def read_user_by_name_controller(self, request: Request):
        users = UserService().read_user_by_name(request.path_params, request.query_params)
        return {"error": False, "data": users}

    def add_user_controller(self, schema: UserSchema):

        newUser = User(
            id=None, 
            name=schema.name, 
            email=schema.email, 
            password=schema.password, 
            card_id=None
        )

        new_user_id: int = UserService().add_user(new_user=newUser.model_dump(exclude_unset=True))
        return {"error": False, "message" : "user added sucessfully", "id": new_user_id}

    def update_user_controller(self, user: user_dependency, id: int, user_to_update: UserEditSchema):
        
        if user.get("id") != id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user can't do this action for another user"
            )

        edited_id = UserService().update_user(id, user_to_update.model_dump(exclude_unset=True))
        return {"error": False, "message" : "user edited sucessfully", "id": edited_id}

    def kill_yourself_controller(self, user: user_dependency, id: int):
    # def delete_user_controller(self, id: int):
        
        if user.get("id") != id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user can't do this action for another user"
            )

        deleted_id = UserService().kill_yourself(id=id) # UserService().delete_user(id=id)
        return {"error": False, "message" : "user deleted sucessfully", "id": deleted_id}
