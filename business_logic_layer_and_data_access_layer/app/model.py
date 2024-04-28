from pydantic import BaseModel, EmailStr, Field

# 定义用于接收用户输入的模型
class UserModel(BaseModel):
    username: EmailStr
    password: str  # 用户创建账户时输入的明文密码

class UserCreateModel(UserModel):
    # 如果创建用户时需要更多字段，可以在这里添加
    pass

class UserUpdateModel(BaseModel):
    password: str  # 用于更新密码的模型

class UserInDBModel(BaseModel):
    username: EmailStr
    hashed_password: str  # 存储在数据库中的散列密码