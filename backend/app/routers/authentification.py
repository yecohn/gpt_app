from fastapi import APIRouter, Depends
from backend.app.models import *
from .token import *
from fastapi.security import OAuth2PasswordRequestForm
from backend.engine.gpt import GPTClient
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
async def login(info: OAuth2PasswordRequestForm = Depends()):
    """retreive user from database

    Args:
        username (str): username of user
        password (str): password of user

    Returns:
        : redirect user on chat page with previous chat
    """
    user = UserInfo.retrieve_user_info_based_on_username(username=info.username)
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
async def signup(inf: Userinf):
    """_summary_

    Args:
        inf (Userinf): _description_
        db (_type_, optional): _description_. Defaults to Depends(access_sql).

    Returns:
        _type_: _description_
    """
    
    user_id = UserInfo.add_new_user(inf=inf)

    gpt = GPTClient()

    gpt.initialize_new_chat(chatID=user_id)

    return {"message": "user and chat created", "success": True}
