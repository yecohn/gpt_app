# app/__init__.py
from .relational_database import engine
from .relational_tables import Base
 
Base.metadata.create_all(bind=engine)