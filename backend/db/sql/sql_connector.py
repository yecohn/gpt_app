from typing import Any, Callable, Iterable
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from google.cloud.sql.connector import Connector
import json
from google.auth import load_credentials_from_file



Base = declarative_base()

connector = Connector()


# function to return the database connection object
def getengine():
    def getconn():
        with open("./config/config.json", "r") as f:
            SQL_CONF = json.load(f)
        DB_HOST = SQL_CONF["INSTANCE_CONNECTION_NAME"]
        DB_USER = SQL_CONF["DB_USER"]
        DB_PASS = SQL_CONF["DB_PASS"]
        DB_NAME = SQL_CONF["DB_NAME"]
        # DB_PORT = SQL_CONF["DB_PORT"]
        conn = connector.connect(
            DB_HOST, "pg8000", user=DB_USER, password=DB_PASS, db=DB_NAME
        )
        return conn

    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return engine


class SQLConnector:
    def __init__(self) -> None:
        engine = getengine()
        self.session = sessionmaker(bind=engine)()

    def commit_session(func: Callable) -> Callable:
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            func(self, *args, **kwargs)
            self.session.commit()

        return wrapper

    @commit_session
    def add(self, Table: Base):
        """add  object Table to the database
        Args:
            Table (Base): Object of database
        """
        self.session.add(Table)

    @commit_session
    def remove(self, Table: Base, args: Iterable):
        pass

    def find(self, Table: Base, query: str) -> Base:
        pass
