from fastapi import FastAPI
from backend.gpt import GPTClient
from backend.speech_to_text import STT
from backend.text_to_speech import TTS

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to our app to learn english"}


@app.get("/chat")
def answer():
    return {"message": "wecome to chat page"}
