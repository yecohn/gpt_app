from pymongo import MongoClient
import json

CONFIG_PATH = "./config/config.json"


class MongoConnector:
    def __init__(self, db_name):
        self.client = MongoClient(self.secret)
        self.db = self.client[db_name]
        print("initialized db connector")

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
        result = self.db[f"{collection_name}"].find_one(query)
        return result
    
    def find_all_but(self, collection_name, projection):
        result = self.db[f"{collection_name}"].find({}, projection)
        return result

    def push(self, collection_name, query, setter):
        self.db[collection_name].update_one(query, setter)

    def find_all(self, query, collection_name):
        result = self.db[f"{collection_name}"].find(query)
        return result


def access_mongo():
    try:
        mongo_client = MongoConnector("speakit")
        yield mongo_client
    finally:
        mongo_client.client.close()


if __name__ == "__main__":
    db = MongoConnector("speakit")
    # db.push({"test": "test"})
    # db.find(collection_name="chats", query={"user_id": 1})
    # print(db.find(collection_name="topics", query={"topic_id": 1}))
    # print(db.find_all_but(collection_name="topics", projection = {"transcript": 0}))
    # print(db.find({"test": "test"}))
    # db.delete({"test": "test"})
    # db.update({"test": "test"}, {"test": "test2"})
