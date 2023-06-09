from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
import moviepy.editor as moviepy
from .routers import user, chat, authentification, topic, lesson, message
from .oauth2 import get_current_user

app = FastAPI()
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(authentification.router)
app.include_router(topic.router)
app.include_router(lesson.router)
app.include_router(message.router)
message = ""


# meir = UserInfo("Meir Lejzerowicz", mongo_client)


origins = ["http://0.0.0.0:3000", "0.0.0.0:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "welcome to our app to learn french"}


# TODO: add a websocket to stream audio to the frontend

