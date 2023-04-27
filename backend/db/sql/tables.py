from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from backend.db.sql.sql_connector import connect_tcp_socket

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column("username", String(50))
    email = Column("email", String(50))
    age = Column("age", Integer)
    occupation = Column("occupation", String(50))
    location = Column("City", String(50))
    level = Column("level", String(50))
    native = Column("native language", String(50))


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    language = Column("language", String(50))
    start_date = Column("start_date", Date)
    last_date = Column("last_date", Date)
    user = relationship("User", back_populates="chats")


if __name__ == "__main__":
    engine = connect_tcp_socket()
    Base.metadata.create_all(bind=engine)
