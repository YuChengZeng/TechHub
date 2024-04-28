from pymongo import MongoClient
from typing import List
from model import UserCreateModel, UserInDBModel
from common import get_logger

logger = get_logger()

class UserDAL:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, user: UserCreateModel) -> UserInDBModel:
        user_dict = user.dict()
        user_dict["hashed_password"] = self.hash_password(user_dict.pop("password"))
        self.collection.insert_one(user_dict)
        return UserInDBModel(**user_dict)

    def find_user(self, username: str) -> UserInDBModel:
        user = self.collection.find_one({"username": username})
        if user:
            return UserInDBModel(**user)
        return None

    def update_password(self, username: str, new_password: str):
        hashed_password = self.hash_password(new_password)
        self.collection.update_one({"username": username}, {"$set": {"hashed_password": hashed_password}})

    def delete_user(self, username: str):
        self.collection.delete_one({"username": username})

    @staticmethod
    def hash_password(password: str) -> str:
        # Use bcrypt or any other hash algorithm to hash passwords
        return "hashed_" + password