from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from common import get_logger

logger = get_logger()

class MongoDBManager:
    """
        專門處理DB連線、初始化
    """
    mongo_url = "mongodb://mongodb:27017/"
    db_name = "mydatabase"
    client = None
    db = None

    @classmethod
    def connect(cls):
        logger.info(f'cls.client--{cls.client}')
        if cls.client is None:
            try:
                cls.client = MongoClient(cls.mongo_url, serverSelectionTimeoutMS=5000)
                cls.db = cls.client[cls.db_name]  # 初始化
                # 進行連線測試
                info = cls.client.server_info()
                print("Successfully connected to MongoDB!")
                print("MongoDB Server Info:", info)
                return True
            except ConnectionFailure:
                print("MongoDB 連線失敗")
                cls.client = None
                cls.db = None
                return False
        else:
            print("MongoDB 已連線")
            return True

    @classmethod
    def get_db(cls):
        if cls.db is None and cls.client is not None:
            cls.db = cls.client[cls.db_name]
        return cls.db

    @classmethod
    def get_status(cls):
        logger.info(f'cls.client--{cls.client}')
        if cls.client:
            try:
                # 進行連線測試
                info = cls.client.server_info()
                print("MongoDB Server Info:", info)
                return "connected"
            except ConnectionFailure:
                return "disconnected"
        else:
            return "disconnected"

    @classmethod
    def close_connection(cls):
        """
            測試用，MongoDB 不需要主動關閉連線
        """
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None  # 關閉連線時也重置數據庫實例
            print(f"MongoDB 連線已關閉")
            return True
        return False
