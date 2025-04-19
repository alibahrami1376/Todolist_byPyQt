from models.db.user_entity import UserEntity
from services.db_session import SessionLocal
from sqlalchemy.exc import NoResultFound
from typing import Optional

class UserViewModel:
    def __init__(self):
        self.db = SessionLocal()

    def create_user(self, username: str, password: str) -> UserEntity:
        user = UserEntity(username=username, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        try:
            return self.db.query(UserEntity).filter(UserEntity.username == username).one()
        except NoResultFound:
            return None

    def delete_user(self, user_id: str):
        user = self.db.get(UserEntity, user_id)
        if user:
            self.db.delete(user)
            self.db.commit()


    def validate_credentials(self, user: str, passw: str) -> Optional[UserEntity]:
        _user = self.db.query(UserEntity).filter_by(username=user, password=passw).first()
        return _user   
