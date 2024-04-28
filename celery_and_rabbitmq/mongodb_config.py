from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self):
        mongo_url = os.getenv('MONGO_URL', 'mongodb://mongodb:27017')
        self.client = MongoClient(mongo_url)
        self.db = self.client['mydatabase']
        self.collection = self.db['mycollection']

    def get_collection(self):
        return self.collection
