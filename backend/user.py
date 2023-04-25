import json
DB_PATH = "./backend/db.json"

class User:
    def __init__(self, username) -> None:
        self.username = username
        self.retrieve_personal_info()
        # in python class are camelCase: MyClass and functions are snake_case: my_function

    def retrieve_personal_info(self):
        with open(DB_PATH, "r") as f:
            users = json.load(f).get("Users")
            user = users[self.username]
            print(user)
            return [setattr(self, k, v) for k, v in user.items()]

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


if __name__ == "__main__":
    user = User("Meir")
    user.update_personal_info("level", "intermediate")
    user.update_personal_info("level", "beginner")
