
from typing import Optional


from models.db.task_entity import TaskEntity
from services.db_session import get_session
from models.db.user_entity import UserEntity

class UserService:
    def __init__(self):
        pass

    def create_user(self, user : UserEntity) -> UserEntity:
        with get_session() as db :
            db.add(user)
            db.commit()
            db.refresh(user)
            return user 
            

    # def get_user_by_username(self, username: str) -> Optional[UserEntity]:
    #     try:
    #         return self.db.query(UserEntity).filter(UserEntity.username == username).one()
    #     except NoResultFound:
    #         return None

    # def delete_user(self, user_id: str):
    #     user = self.db.get(UserEntity, user_id)
    #     if user:
    #         self.db.delete(user)
    #         self.db.commit()


    def validate_credentials(self, user: str) -> Optional[UserEntity]:
        with get_session() as db:
            _user = db.query(UserEntity).filter_by(username=user).first()
            # print(_user)
            return _user