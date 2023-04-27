from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

with open('config.json', 'r') as f:
    DATABASE_URL = json.load(f).get('sql_uri')

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

Session = sessionmaker(bind=engine)


