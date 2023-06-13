from backend.db.mongo.mongo_connector import MongoConnector
from backend.app.users.hashing import Hash
from backend.app.models import Userinf
from bson.objectid import ObjectId
from fastapi import HTTPException

class UserInfo:
    db_connector = MongoConnector('speakit')

    def __init__(
        self
    ):
        pass

    @classmethod
    def retrieve_user_info_based_on_username(cls, username: str):
        return cls.db_connector.find(
            query = {'username': username}, 
            collection_name = 'users'
            )
    
    # login classmethod
    @classmethod
    def login(cls, username: str, password: str):
        user = cls.retrieve_user_info_based_on_username(username=username)
        if not user:
            raise HTTPException(
                status_code=400, detail='User not found'
            )
        if not Hash.verify(user['password'], password):
            raise HTTPException(
                status_code=400, detail='Incorrect password'
            )
        return str(user['_id'])

    @classmethod
    def retrieve_username(cls, user_id: str):
        # write a call to mongDB to retrieve username
        return cls.db_connector.find(
            query = {'_id': ObjectId(user_id)}, 
            collection_name = 'users'
            )['username']
    
    
    @classmethod
    def add_new_user(cls, inf : Userinf):
        
        insertion = cls.db_connector.insert_one(
            data = {
                'username': inf.username,
                'password': Hash.bcrypt(inf.password),
                'native': inf.native,
                'target': inf.target,
            },
            collection_name='users'
        )
        user_id = str(insertion.inserted_id)
        
        return user_id


# from backend.db.sql.sql_connector import SQLConnector, access_sql
# from backend.db.sql.tables import User
# from backend.app.users.hashing import Hash
# from backend.app.models import Userinf

# class UserInfo:
#     db_connector = SQLConnector()
    
#     def __init__(
#         self, 
#         userid: str, 
#     ):
#         self.userid = userid
#         self.retrieve_personal_info()
#         # in python class are camelCase: MyClass and functions are snake_case: my_function

#     @classmethod
#     def retrieve_user_info_based_on_username(cls, username: str):
#         return cls.db_connector.query(User, query= User.username == username)
        

#     def retrieve_personal_info(self):
#         user = self.db_connector.query(User, User.id == self.userid)
#         [setattr(self, k, v) for k, v in user.__dict__.items()]

#     def update_personal_info(self, attr, val):
#         NotImplemented

#     @classmethod
#     def add_new_user(cls, inf : Userinf):
#     # username: str, password: str, email: str, level: str):
#         cls.db_connector.add(
#             User(
#                 username=inf.username,
#                 password=Hash.bcrypt(inf.password),
#                 # email=inf.email,
#                 # level=inf.level,
#             )
#         )
#         # return id of added user
#         return cls.db_connector.query(User, query=User.username == inf.username).id
