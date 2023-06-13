from fastapi import APIRouter, Depends
from backend.app.models import Userinf
from .token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from backend.engine.gpt import GPTClient
from backend.app.users.user import UserInfo

router = APIRouter(tags=["AUTHENTIFICATION"])
gpt = GPTClient()

@router.post("/login")
async def login(info: OAuth2PasswordRequestForm = Depends()):
    username = info.username
    password = info.password

    user_id = UserInfo.login(username=username, password=password)
    
    access_token = create_access_token(
        data={"sub": info.username},
    )
    chatId = gpt.retrieve_chatId(user_id=user_id)
    
    res =  {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "chatId": chatId
    }
    
    
    return res
        

    


@router.post("/register", status_code=200)
async def signup(inf: Userinf):
    
    user_id = UserInfo.add_new_user(inf=inf)
    print(user_id)

    chatId = gpt.initialize_new_chat(user_id=user_id, inf=inf)
    res = {
        "message": "user created",
        "success": True,
        "user_id": user_id,
        "chat_id": chatId,
    }
    return res



# def formulate_message(user_id: int, user_name: str, origin: str, text: str, date: datetime):
#     message = {
#         "user": {"id": user_id, "name": user_name},
#         'origin': origin,
#         "text": text,
#         "createdAt": date,
#     }
#     return message