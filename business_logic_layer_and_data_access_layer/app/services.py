from typing import List, Optional
from dal import UserDAL
from model import UserCreateModel, UserUpdateModel
from common import get_logger
logger = get_logger()

class UserService:
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    def register_user(self, user_data: UserCreateModel):
        if self.user_dal.find_user(user_data.username) is not None:
            raise ValueError("User already exists")
        return self.user_dal.create_user(user_data)

    def authenticate_user(self, username: str, password: str):
        user = self.user_dal.find_user(username)
        if user and user.hashed_password == self.user_dal.hash_password(password):
            return True
        return False

    def change_password(self, username: str, password_data: UserUpdateModel):
        return self.user_dal.update_password(username, password_data.password)

    def remove_user(self, username: str):
        self.user_dal.delete_user(username)