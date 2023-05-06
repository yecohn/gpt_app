from pymongo import MongoClient
import json

CONFIG_PATH = "/Users/yosh/Desktop/projects/gpt/config/config.json"


class DBConnector:
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

    def push(self, data, collection_name):
        self.db[collection_name].insert_one(data)

    def delete(self, data, collection_name):
        self.db[collection_name].delete_one(data)

    def update(self, data, new_data, collection_name):
        setter = {"$set": new_data}
        self.db[collection_name].update_one(data, setter)

    def find(self, query, collection_name):
        return self.db[collection_name].find_one(query)


def access_mongo():
    try:
        mongo_client = DBConnector("chat")
        yield mongo_client
    finally:
        mongo_client.db.close()


if __name__ == "__main__":
    db = DBConnector("speakit", "test")
    db.push({"test": "test"})
    print(db.find({"test": "test"}))
    db.delete({"test": "test"})
    db.update({"test": "test"}, {"test": "test2"})
