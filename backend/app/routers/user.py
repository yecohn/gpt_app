from fastapi import APIRouter
from backend.db.sql.sql_connector import SQLConnector

# can add prefix="/user" to all routes
router = APIRouter()
sql_client = SQLConnector()





