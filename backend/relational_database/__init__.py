# app/__init__.py
from .database import engine
from .tables import Base
 
Base.metadata.create_all(bind=engine)