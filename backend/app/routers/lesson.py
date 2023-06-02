from fastapi import APIRouter, Depends
from backend.db.mongo.mongo_connector import access_mongo, MongoConnector
from backend.engine.gpt import GPTClient

router = APIRouter()


@router.get('/lesson/', status_code=200)
async def topic_list(
    mongo_db: MongoConnector = Depends(access_mongo),
):
    gpt = GPTClient()
    lesson_prompt = mongo_db.find({}, "metadata")["GPT_metadata"]["lesson_prompt_template"]

    lesson = gpt.create_lesson(lesson_prompt)
    
    res = lesson
    return res