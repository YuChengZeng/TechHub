from pymongo import MongoClient
from typing import List
from model import ItemModel

class ItemDAL:
    def __init__(self, db):
        self.collection = db.items

    # 新增一筆資料到DB，若id已存在則回傳None
    def create_item(self, item: ItemModel):
        if self.collection.find_one({"id": item.id}):
            return None
        self.collection.insert_one(item.dict())
        return item

    # 使用find_one尋找對應id並回傳，若無則None
    def get_item(self, item_id: int):
        item = self.collection.find_one({"id": item_id}, {"_id": 0})
        return item

    # 尋找items所有資料
    def get_all_items(self) -> List[ItemModel]:
        items = list(self.collection.find({}, {"_id": 0}))
        return items