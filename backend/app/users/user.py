from backend.db.sql.sql_connector import SQLConnector, access_sql
from backend.db.sql.tables import User
from fastapi import Depends
from backend.app.users.hashing import Hash
from backend.app.models import Userinf

class UserInfo:
    def __init__(
        self, 
        userid: str, 
    ):
        self.userid = userid
        self.db_connector: SQLConnector = Depends(access_sql)
        self.retrieve_personal_info()
        # in python class are camelCase: MyClass and functions are snake_case: my_function

    def retrieve_user_info_based_on_username(self, username: str):
        return self.db_connector.query(User, query= {User.username == username})
        

    def retrieve_personal_info(self):
        user = self.db_connector.query(User, User.id == self.userid)
        [setattr(self, k, v) for k, v in user.__dict__.items()]

    def update_personal_info(self, attr, val):
        NotImplemented

    @classmethod
    def add_new_user(cls, inf : Userinf):
    # username: str, password: str, email: str, level: str):
        cls.db_connector.add(
            User(
                username=inf.username,
                password=Hash.bcrypt(inf.password),
                email=inf.email,
                level=inf.level,
            )
        )
        # return id of added user
        return cls.db_connector.query(User, query=User.username == inf.username).id
