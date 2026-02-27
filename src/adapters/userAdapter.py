from src.models.userModel import User
from src.schemas.userSchema import UserSchema
from src.services.userService import UserService

class UserAdapter:

    def read_all_users_controller(self):
        return UserService().read_all_users()


    def add_user_controller(self, schema: UserSchema):

        newUser = User(
            id=None, 
            name=schema.name, 
            email=schema.email, 
            password=schema.password, 
            card_id=None
        )

        UserService().add_user(new_user=newUser)