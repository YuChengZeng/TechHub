from typing import List, Optional
from dal import ItemDAL
from model import ItemModel

class ItemService:
    def __init__(self, item_dal: ItemDAL):
        self.item_dal = item_dal

    # 使用DAL的create_item創建一筆資料
    def create_item(self, item: ItemModel) -> Optional[ItemModel]:
        return self.item_dal.create_item(item)

    # 使用DAL的get_item搜尋id的資料
    def get_item(self, item_id: int) -> Optional[ItemModel]:
        return self.item_dal.get_item(item_id)

    # 使用DAL的get_all搜尋所有資料
    def get_all_items(self) -> List[ItemModel]:
        return self.item_dal.get_all_items()