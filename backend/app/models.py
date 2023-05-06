from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Userinf(BaseModel):
    username: str
    email: str
    password: str
    level: str


class Logininf(BaseModel):
    username: str
    password: str


class Item(BaseModel):
    title: str


class AudioUrl(BaseModel):
    audiourl: str


class TokenData(BaseModel):
    username: str 