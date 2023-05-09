from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.db.sql.sql_connector import access_sql
from backend.db.sql.tables import User
from backend.app.models import *
from backend.app.users.hashing import Hash
from .token import *
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["AUTHENTIFICATION"])


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
    print(user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not Hash.verify(user.password, password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token = create_access_token(
        data={"sub": user.username},
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
    }


@router.post("/register", status_code=200)
async def signup(inf: Userinf, db=Depends(access_sql)):
    """create user in database

    Args:
        username (str): _description_
        password (str): _description_

    Returns:
        _type_: redirect user on chat page with previous chat
    """
    print(inf.username, inf.password, inf.email)

    db.add(
        User(
            email=inf.email,
            password=Hash.bcrypt(inf.password),
            username=inf.username,
            level=inf.level,
        )
    )
    return {"message": "user created", "success": True}
