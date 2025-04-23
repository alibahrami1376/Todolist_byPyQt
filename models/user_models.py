from uuid import uuid4
from typing import Optional



class UserModel:
    def __init__(
        self,
        username: str,
        password: str,
        email_address: Optional[str]=None,
        phone_number: Optional[str]=None,
        is_activate: Optional[bool]=None, 
        ):
        self.username= username 
        self.password= password
        self.id= uuid4().hex
        self.email_address= email_address
        self.phone_number= phone_number
        self.is_activate= is_activate

    def get_pass(self) -> str:
        return self.password
    def set_pass(self,password:str) :
        self.password = password

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email_address,
            "phonenumber": self.phone_number,
            "is_activate": self.is_activate,
        }

    @staticmethod
    def from_dict(data: dict) -> "UserModel":
        return UserModel(
        username= data.get("username") ,
        password= data.get("password"),
        email_address= data.get("email",""),
        phone_number= data.get("phone",""),
        is_activate= data.get("is_activate",False), 
        )


