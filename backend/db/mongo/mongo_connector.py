from pymongo import MongoClient
import json

CONFIG_PATH = "./config/config.json"


class MongoConnector:
    def __init__(self, db_name):
        self.client = MongoClient(self.secret)
        self.db = self.client[db_name]

    @property
    def secret(cls):
        return cls.__get_secret()

    def __get_secret(self):
        with open(CONFIG_PATH, "r") as f:
            secret = json.load(f).get("mongo_uri")
        return secret

    def insert_one(self, data, collection_name):
        collection = self.db[collection_name]
        insertOneResult = collection.insert_one(data)
        return insertOneResult
        

    def delete_one(self, data, collection_name):
        collection = self.db[collection_name]
        collection.delete_one(data)

    def update_one(self, query, setter, collection_name):
        collection = self.db[collection_name]
        collection.update_one(query, setter)

    def find(self, query, collection_name, projection = None):
        collection = self.db[collection_name]
        return collection.find_one(query)
    
    def find_all(self, collection_name):
        collection = self.db[collection_name]
        return collection.find()
    
    # def find_all_but(self, collection_name, projection):
    #     result = self.db[f"{collection_name}"].find({}, projection)
    #     return result

    # def push(self, collection_name, query, setter):
    #     self.db[collection_name].update_one(query, setter)




def access_mongo():
    try:
        mongo_client = MongoConnector("speakit")
        yield mongo_client
    finally:
        mongo_client.client.close()


if __name__ == "__main__":
    db = MongoConnector("speakit")
