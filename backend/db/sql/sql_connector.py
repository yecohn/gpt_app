from backend.db.sql.tables import Base
from typing import Any, Callable, Iterable
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from config.config import SQL_CONF


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of Postgres."""
    db_host = SQL_CONF["INSTANCE_CONNECTION_NAME"]
    db_user = SQL_CONF["DB_USER"]
    db_pass = SQL_CONF["DB_PASS"]
    db_name = SQL_CONF["DB_NAME"]
    db_port = SQL_CONF["DB_PORT"]

    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
    )
    return engine


class SQLConnector:
    def __init__(self) -> None:
        engine = connect_tcp_socket()
        self.session = sessionmaker(bind=engine)()

    def commit_session(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func(*args, **kwargs)
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


