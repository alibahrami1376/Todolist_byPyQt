from models.db.user_entity import UserEntity
from services.db_session import SessionLocal
from sqlalchemy.exc import NoResultFound
from typing import Optional

from services.user_service import UserService
from models.user_models import UserModel
from mapper.user_mapper import map_model_to_entity
from mapper.user_mapper import map_entity_to_model
from utils.security import hash_password,check_password
class UserViewModel:
    def __init__(self):
        self.UserService = UserService()
    

    def validate_credentials(self,username: str,password: str) -> Optional[UserModel]:
        user = self.UserService.validate_credentials(username)
        if user :
            if check_password(password,user.password):
                return map_entity_to_model(user)
        return None


    def register_dict(self,data: dict) -> UserModel :
        data["password"] = hash_password (data.get("password")) 
        user_model = UserModel.from_dict(data)
        self.UserService.create_user(map_model_to_entity(user_model))
        return user_model 


    def creat_guest(self):
        return UserModel(username="GUEST",password="")