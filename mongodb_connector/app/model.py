from pydantic import BaseModel

# 定義DB中的model
class ItemModel(BaseModel):
    id: int
    name: str