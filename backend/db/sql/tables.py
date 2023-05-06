from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from backend.db.sql.sql_connector import getengine
from sqlalchemy.orm import declarative_base

# BEFORE RUNNING THIS SCRIPT ADD ENV VARIABLE:
# export GOOGLE_APPLICATION_CREDENTIALS="<path_to_project>/config/sql_credentials.json"
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(50))
    email = Column("email", String(50))
    level = Column("level", String(50))
    # native = Column("native language", String(50))
    password = Column("password", String(200))


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    language = Column("language", String(50))
    start_date = Column("start_date", Date)
    last_date = Column("last_date", Date)
    # user = relationship("User", back_populates="chats")


if __name__ == "__main__":
    engine = getengine()
    Base.metadata.create_all(bind=engine)
