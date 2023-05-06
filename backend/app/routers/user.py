from fastapi import APIRouter
from pydantic import BaseModel
from backend.db.sql.sql_connector import SQLConnector
from backend.db.sql.tables import User
from backend.app.users.hashing import Hash


# can add prefix="/user" to all routes
router = APIRouter()
sql_client = SQLConnector()





