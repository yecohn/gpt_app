# app/__init__.py
import os
from backend.relational_database.relational_tables import Base
from backend.rel_db_connector import engine



Base.metadata.create_all(bind=engine)
