# app/__init__.py
import os
from backend.relational_database.tables import Base
from backend.rel_db_connector import engine



Base.metadata.create_all(bind=engine)
