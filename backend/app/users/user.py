import json
import enum
from backend.db.mongo.mongo_connector import DBConnector

DB_PATH = "./backend/db.json"


class User:
    def __init__(self, username: str, db_connector: DBConnector) -> None:
        self.username = username
        self.db_connector = db_connector
        self.retrieve_personal_info()
        # in python class are camelCase: MyClass and functions are snake_case: my_function

    def retrieve_personal_info(self):
        user = self.db_connector.find({"name": self.username}, "users")
        [setattr(self, k, v) for k, v in user.items()]

    def update_personal_info(self, attr, val):
        with open(DB_PATH, "r") as f:
            db = json.load(f)

        users = db.get("users")
        user = users.get(self.username)
        # TODO: add recursive function that will update nested dict (will be replace by real db)
        user[attr] = val
        users[self.username] = user
        db["Users"] = users

        with open(DB_PATH, "w") as f:
            json.dump(db, f)
        self.retrieve_personal_info()


class Level(enum.Enum):
    BEGINNER = {
        "gpt": {
            # "frequency_penalty": -2,
            "presence_penalty": 0,
            "temperature": 0.2,
            "stop": "? ",
            # "stream": False,
        },
        "tts": {"speech_rate": 0.05},
    }


if __name__ == "__main__":
    user = User("Meir")
    user.update_personal_info("level", "intermediate")
    user.update_personal_info("level", "beginner")
