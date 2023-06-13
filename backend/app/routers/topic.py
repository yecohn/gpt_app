from fastapi import APIRouter, Depends
from backend.db.mongo.mongo_connector import access_mongo, MongoConnector
from backend.engine.gpt import GPTClient


router = APIRouter()
gpt = GPTClient()


@router.get("/topics", status_code=200)
async def topic_list(
    mongo_db: MongoConnector = Depends(access_mongo),
):
    """_summary_

    Args:
        mongo_db (_type_, optional): _description_. Defaults to Depends(access_mongo).

    Returns:
        _type_: _description_
    """
    # get chat language from chat id

    topics = mongo_db.find_all(    
        collection_name="topics",
    )

    res = []
    for topic in topics:
        res.append(
            {
                "topic_id": topic["topic_id"],
                "name": topic["name"],
                "description": topic["description"],
                "link": topic["link"],
            }
        )
    return res


@router.get("/chat/{chatId}/topics/{topic_id}", status_code=200)
async def triggerTopic(chatId: str, topic_id: int):
    
    gpt.trigger_topic(chatId=chatId, topic_id=topic_id)
    return {"message": "topic triggered", "success": True}
