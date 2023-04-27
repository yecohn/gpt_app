from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()
 
class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column('username', String(50))
    email = Column('email', String(50))
    age = Column('age', Integer)
    occupation = Column('occupation', String(50))
    location = Column('City', String(50))
    level = Column('level', String(50))
    native = Column('native language', String(50))



class Chat(Base):

    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    language = Column('chat language', String(50))
    start_date = Column('start date', date)
    last_date = Column('last chat date', date)

    user = relationship('User', back_populates='chats')
    