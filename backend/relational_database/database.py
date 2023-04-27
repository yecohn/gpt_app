from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from config import SQL_CONF


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of Postgres."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
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


engine = connect_tcp_socket()
Session = sessionmaker(bind=engine)
