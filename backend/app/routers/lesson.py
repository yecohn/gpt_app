from fastapi import APIRouter, Depends
from backend.db.mongo.mongo_connector import access_mongo, MongoConnector
from backend.engine.gpt import GPTClient

router = APIRouter()
gpt = GPTClient()


@router.get('/chat/{user_id}/lesson', status_code=200)
async def generate_lesson(
    user_id: int,
):

    lesson = gpt.generate_lesson(chatId=user_id)
    
    res = lesson
    return {"lesson": res, "success": True}