import os
from datetime import datetime
from pymongo import MongoClient
from src.config.system_config import SystemConfig

class DataStorage:
    def __init__(self):
        self.client = MongoClient(SystemConfig.MONGO_URI)
        self.db = self.client[SystemConfig.MONGO_DB]
        
    def store_data(self, data):
        """存储爬取的数据"""
        self.db.crawled_data.insert_one(data)
        
    def query_data(self, query):
        """查询数据"""
        return self.db.crawled_data.find(query)
    
    def _save_to_local(self, data):
        """Windows兼容的本地存储方法"""
        data_dir = os.path.join("data", "crawled_data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(str(data))
