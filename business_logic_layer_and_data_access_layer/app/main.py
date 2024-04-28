from fastapi import FastAPI, HTTPException, Query, Depends
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from model import UserCreateModel, UserUpdateModel # model
from dal import UserDAL # DAL
from services import UserService # BLL
from common import get_logger
logger = get_logger()

app = FastAPI()

# MongoDB
MONGO_URL = "mongodb://mongodb:27017/"
client = MongoClient(MONGO_URL)
db = client["mydatabase"]

user_dal = UserDAL(db=db)
user_service = UserService(user_dal=user_dal)

@app.post("/users/")
def create_user(user: UserCreateModel):
    try:
        return user_service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login/")
def login(username: str, password: str):
    if user_service.authenticate_user(username, password):
        return {"message": "User authenticated"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.put("/users/{username}")
def update_user(username: str, password: UserUpdateModel):
    return user_service.change_password(username, password)

@app.delete("/users/{username}")
def delete_user(username: str):
    user_service.remove_user(username)
    return {"message": "User deleted"}