from fastapi import APIRouter, Depends
from backend.db.sql.sql_connector import access_sql
from backend.db.mongo.mongo_connector import access_mongo, MongoConnector
from backend.db.sql.tables import User
from backend.app.models import *
from backend.app.users.hashing import Hash
from .token import *
from fastapi.security import OAuth2PasswordRequestForm
from backend.engine.gpt import GPTClient
import openai
from datetime import datetime
from backend.app.users.user import UserInfo


router = APIRouter(tags=["AUTHENTIFICATION"])

def formulate_message(user_id: int, user_name: str, origin: str, text: str, date: datetime):
    message = {
        "user": {"id": user_id, "name": user_name},
        'origin': origin,
        "text": text,
        "createdAt": date,
    }
    return message

@router.post("/login")
async def login(info: OAuth2PasswordRequestForm = Depends(), db=Depends(access_sql)):
    """retreive user from database

    Args:
        username (str): username of user
        password (str): password of user

    Returns:
        : redirect user on chat page with previous chat
    """
    username, password = info.username, info.password
    user = db.query(User, query=User.username == username)
    # print(user.id)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    #     )
    # if not Hash.verify(user.password, password):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
    #     )
    access_token = create_access_token(
        data={"sub": user.username},
    )


    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
    }


@router.post("/register", status_code=200)
async def signup(
    inf: Userinf, 
    sql_db=Depends(access_sql), 
    mongo_db: MongoConnector = Depends(access_mongo)
    ):
    """_summary_

    Args:
        inf (Userinf): _description_
        db (_type_, optional): _description_. Defaults to Depends(access_sql).

    Returns:
        _type_: _description_
    """
    print(inf.username, inf.password, inf.email, inf.level)

    sql_db.add(
        User(
            email=inf.email,
            password=Hash.bcrypt(inf.password),
            username=inf.username,
            level=inf.level,
            # native=inf.native,
            # target=inf.target,
        )
    )
    user_id = sql_db.query(User, query=User.username == inf.username).id
    
    
    initial_prompt = mongo_db.find({}, "metadata")["GPT_metadata"]["initial_prompt_template"]

    initial_prompt['native_language'] = 'English'
    initial_prompt['target_language'] = 'Hebrew'
    initial_prompt['user']['name'] = inf.username
    initial_prompt['user']['level'] = 'Beginner'
    initial_prompt['parameters']['level'] = 'Beginner'

    chat = {
        'user_id': user_id,
        'chat_id': user_id,
        'messages': [],
        'initial_prompt': initial_prompt,
    }
    mongo_db.insert_one(chat, "chats")

    usr = UserInfo(userid=user_id, db_connector=sql_db)
    gpt = GPTClient(user=usr, db_connector=mongo_db)
    openai.api_key = gpt.api_key
    answer = gpt.ask_gpt(initial_prompt)
    answer_json = formulate_message(user_id, 'ai', 'system', answer, datetime.now())

    mongo_db.push(
        collection_name="chats",
        query={"user_id": user_id},
        setter={"$push": {"messages": answer_json}},
    )
    return {"message": "user and chat created", "success": True}
