from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50))
    email = Column("email", String(50))
    age = Column("age", Integer)
    profession = Column("profession", String(50))

    def __init__(self, id, name, email, age, profession):
        self.id = id
        self.name = name
        self.email = email
        self.age = age
        self.profession = profession

    def __repr__(self):
        return f"(id={self.id}, name={self.name}, email={self.email}, age={self.age})"

# class 

engine = create_engine("sqlite:///users.db", echo=True)
# Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
# person = User(1, "Meir", "meir.lezj@gmail.com", 28, "engineer")
# session.add(person)
# session.commit()

res = session.query(User).filter(User.name == "Meir").all()
print(res)
