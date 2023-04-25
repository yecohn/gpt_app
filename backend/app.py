from fastapi import FastAPI, File, UploadFile, Form, WebSocket
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import audiosegment
import openai
import sounddevice as sd
import wavio as wv
from google.cloud import speech
import os
import io
from typing import Type
import numpy as np
import requests
from backend.gpt import GPTClient
from backend.speech_to_text import STT
from backend.text_to_speech import GCPTTS
from backend.user import User
import shutil
import moviepy.editor as moviepy
from pathlib import Path
import time
from backend.websocket_manager import ConnectionManager
from datetime import datetime
import json


message = ""
app = FastAPI()
manager = ConnectionManager()
from pydantic import BaseModel

print(os.getcwd())


class Item(BaseModel):
    title: str


class AudioUrl(BaseModel):
    audiourl: str


meir = User("Meir")
gpt = GPTClient(user=meir)
tts = GCPTTS(language="fr-FR", speaker="fr-FR-Wavenet-A")
client = speech.SpeechClient()
freq = 44100
duration = 5
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    audio_channel_count=1,
    language_code="fr-FR",
)
recording_path = "./data/tmp.wav"
recording_path_video = "./data/tmp.webm"
recording_input_path = "./data/input.wav"

stt = STT(
    stt_client=client,
    stt_service=speech.RecognitionAudio,
    stt_config=config,
    freq=freq,
    duration=duration,
    recording_path=recording_path,
)
openai.api_key = gpt.api_key

origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "welcome to our app to learn english"}


@app.post("/")
async def post_root(file: UploadFile):
    with open(recording_path_video, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    clip = moviepy.VideoFileClip(recording_path_video)
    clip.write_audiofile(recording_input_path)
    transcript = stt.get_transcript_from_recording(recording_input_path)
    answer = gpt.ask_gpt(transcript)
    audio_path = tts.generate_speech(answer)
    audio_path = Path(audio_path).resolve()
    print(audio_path)
    return FileResponse(audio_path)
    # return {"file_name": file.filename, "transcript": transcript, "gpt_answer": answer}


@app.get("/chat")
def answer():
    return {"message": "wecome to chat page"}


@app.post("/chat")
async def question(audio: UploadFile):
    start_writing = time.time()
    os.remove(recording_path_video)
    with open(recording_path_video, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    end_writing = time.time()
    duration_write = end_writing - start_writing
    start_converting = time.time()
    os.system(f"ffmpeg -i {recording_path_video} {recording_input_path} -y")
    end_converting = time.time()
    duration_convert = end_converting - start_converting
    start_transcript = time.time()
    transcript = stt.get_transcript_from_recording(recording_input_path)
    end_transcript = time.time()
    duration_transcript = end_transcript - start_transcript
    question = transcript
    start_gpt = time.time()
    answer = gpt.ask_gpt(question)
    global message
    message = answer
    end_gpt = time.time()
    duration_gpt = end_gpt - start_gpt
    print(
        "write took",
        duration_write,
        "seconds",
        "convert took",
        duration_convert,
        "seconds",
        "transcript took",
        duration_transcript,
        "seconds",
        "gpt took",
        duration_gpt,
        "seconds",
        sep="\n",
    )
    _ = tts.generate_speech(answer)
    return {"answer": answer, "transcript": transcript}


# TODO: add a websocket to stream audio to the frontend
######################### We should move to a websocket architecture for streaming audio ################################
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     print("websocket connected")
#     await websocket.accept()
#     data = await websocket.receive_text()
#     print(data)
#     current_message = message
#     while True:
#         if current_message != message:
#             current_message = message
#             print("new message sent")
#             await websocket.send_text(current_message)


# @app.websocket("/ws/")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     now = datetime.now()
#     current_time = now.strftime("%H:%M")
#     while True:
#         data = await websocket.receive_text()
#         # await manager.send_personal_message(f"You wrote: {data}", websocket)
#         message = {"time": current_time, "clientId": client_id, "message": data}
#         await manager.broadcast(json.dumps(message))
