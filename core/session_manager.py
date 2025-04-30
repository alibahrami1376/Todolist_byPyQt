from PyQt6.QtCore import QObject,pyqtSignal
from typing import Optional
from models.user_models import UserModel
from models.task_models import TaskModel

class SessionManager(QObject):
    session_changed= pyqtSignal()
    session_user_set= pyqtSignal()
    session_user_logout= pyqtSignal()
    def __init__(self):
        super().__init__()
        self._current_user: Optional[UserModel] = None
        self._is_guest: bool = False
    



    def set_user(self, user: UserModel):

        self._current_user = user 
        self.session_user_set.emit()
        # self.session_changed.emit()


    def set_guest(self):
        self._is_guest =True
        # self.session_changed.emit()


    def clear_user_current(self):
        if self._is_guest :
            self._is_guest = False
        self._current_user = None
        self.session_user_logout.emit()
        self.session_changed.emit()


    def current_user(self) -> UserModel | None:
        return self._current_user


    def is_guest(self) -> bool:
        return self._is_guest


    def get_id_user(self) -> str:
        return self._current_user.id

# Singleton instance to be used across the app
Session = SessionManager()