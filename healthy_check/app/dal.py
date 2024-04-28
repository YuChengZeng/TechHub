from pymongo import MongoClient
from typing import List
from model import ItemModel
from common import get_logger

logger = get_logger()

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
        # logger.debug(f"ItemDAL get_item: {item_id}")
        # logger.debug(f"ItemDAL type: {type(item_id)}")
        item = self.collection.find_one({"id": item_id}, {"_id": 0})
        return item

    # 尋找items所有資料
    def get_all_items(self) -> List[ItemModel]:
        items = list(self.collection.find({}, {"_id": 0}))
        return items
    
    # 超重要希望不要失敗的 AutoReconnect
    def create_item_with_retry():
        """
            把重要的DB指令放這邊，如果遇到AutoReconnect Error可以做特殊處理
        """
        # 重試的次數 5
        # 重試的間隔 retry^2
        return None

