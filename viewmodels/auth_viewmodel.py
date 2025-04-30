
from typing import Optional

from models.db.user_entity import UserEntity
from services.user_service import UserService
from models.user_models import UserModel
from mapper.user_mapper import map_model_to_entity
from mapper.user_mapper import map_entity_to_model
from utils.security import hash_password,check_password


class UserViewModel:
    def __init__(self,user_service:UserService):
        self.user_service = user_service
    

    def validate_credentials(self,username: str,password: str) -> Optional[UserModel]:
        user = self.fetch_user_entity(username)
        if user :
            if check_password(password,user.password):
                return map_entity_to_model(user)
        return None
    

    def fetch_user_entity(self,username: str)->Optional[UserEntity]:
        return self.user_service.fetch_user(username)
        # try:
        #     entity = self.user_service.validate_credentials(username)
        # except ServiceError as e:
        #     logger.error(f"Failed fetching user: {e}")
        #     return None
        

    def register_dict(self,data: dict) -> UserModel :
        data["password"] = hash_password(data.get("password",None)) 
        user_model = UserModel.from_dict(data)
        self.user_service.create_user(map_model_to_entity(user_model))
        return user_model 


    def create_guest(self)->UserModel:
        return UserModel(username="GUEST",password="")