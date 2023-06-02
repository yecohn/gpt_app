from fastapi import APIRouter, Depends
from backend.db.mongo.mongo_connector import access_mongo, MongoConnector
from backend.engine.gpt import GPTClient
import openai
from datetime import datetime

router = APIRouter()


@router.get("/topics/", status_code=200)
async def topic_list(
    mongo_db: MongoConnector = Depends(access_mongo),
):
    """_summary_

    Args:
        mongo_db (_type_, optional): _description_. Defaults to Depends(access_mongo).

    Returns:
        _type_: _description_
    """
    topics = mongo_db.find_all_but(
        collection_name="topics", projection={"transcript": 0}
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


@router.get("/topics/{topic_id}", status_code=200)
async def triggerTopic(
    topic_id: int,
    user_id: int,
    mongo_db: MongoConnector = Depends(access_mongo),
):
    """_summary_

    Args:
        topic_id (int): _description_
        mongo_db (_type_, optional): _description_. Defaults to Depends(access_mongo).

    Returns:
        _type_: _description_
    """
    gpt = GPTClient()
    openai.api_key = gpt.api_key

    initial_prompt = mongo_db.db['Chats'].find_one({"user_id": messagechat.user.id})['initial_prompt']

    transcript = mongo_db.find(
        collection_name="topics", query={"topic_id": topic_id}
    ).get("transcript")
    topic_prompt = mongo_db.find({}, "metadata")["GPT_metadata"]["topic_prompt_template"]
    topic_prompt['video_summary'] = transcript

    answer = gpt.ask_gpt(initial_prompt, topic_prompt)
    answer_json = {
        "user": {"id": 0, "name": "ai"},
        "text": answer,
        "createdAt": datetime.now(),
    }

    mongo_db.push(
        "chats",
        {"user_id": user_id},
        {"$push": {"messages": answer_json}},
    )

    # _ = tts.generate_speech(answer)
    return {"ok": True}
