from backend.db.sql.sql_connector import SQLConnector, access_sql
from backend.db.sql.tables import User
from fastapi import Depends

class UserInfo:
    def __init__(
        self, 
        userid: str, 
    ):
        self.userid = userid
        self.db_connector: SQLConnector = Depends(access_sql)
        self.retrieve_personal_info()
        # in python class are camelCase: MyClass and functions are snake_case: my_function

    def retrieve_personal_info(self):
        user = self.db_connector.query(User, User.id == self.userid)
        [setattr(self, k, v) for k, v in user.__dict__.items()]

    def update_personal_info(self, attr, val):
        NotImplemented
