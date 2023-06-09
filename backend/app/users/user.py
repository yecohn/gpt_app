from backend.db.sql.sql_connector import SQLConnector
from backend.db.sql.tables import User


class UserInfo:
    def __init__(self, userid: str, db_connector: SQLConnector) -> None:
        self.userid = userid
        self.db_connector = db_connector
        self.retrieve_personal_info()
        # in python class are camelCase: MyClass and functions are snake_case: my_function

    def retrieve_personal_info(self):
        user = self.db_connector.query(User, User.id == self.userid)
        [setattr(self, k, v) for k, v in user.__dict__.items()]

    def update_personal_info(self, attr, val):
        NotImplemented
