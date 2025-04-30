
from typing import Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


from models.db.user_entity import UserEntity


class UserService:
    def __init__(self,session_factory):
        self._session_factory= session_factory 

    def create_user(self, user : UserEntity) -> UserEntity:
        """
        Creating a new user in the database and retrieving the final record
        """
        with self._session_factory() as db:
            try:
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
            except IntegrityError:
                db.rollback()
                # می‌تونی اینجا یک استثنای سفارشی پرتاب کنی:
                raise ValueError("Username already exists")
   

    def fetch_user(self, username: str) -> Optional[UserEntity]:
        """
        Search the database based on username and return the User Entity if it exists.
        """
        with self._session_factory() as db:
            try:
                _user = db.query(UserEntity).filter_by(username=username).first()
                return _user
            except SQLAlchemyError:
                
                return None