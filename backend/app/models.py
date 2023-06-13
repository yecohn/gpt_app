from pydantic import BaseModel
import datetime


class Login(BaseModel):
    username: str
    password: str


class Userinf(BaseModel):
    username: str
    # email: str
    password: str
    # level: str
    native: str
    target: str


class Logininf(BaseModel):
    username: str
    password: str

class TranslationInfo(BaseModel):
    word: str


class Item(BaseModel):
    title: str


class AudioUrl(BaseModel):
    audiourl: str


class TokenData(BaseModel):
    username: str


class Usr(BaseModel):
    id: str
    username: str


class MessageChat(BaseModel):
    user: Usr
    text: str
    createdAt: datetime.datetime
