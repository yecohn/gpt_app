from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

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
from backend.text_to_speech import TTS
import shutil

app = FastAPI()
from pydantic import BaseModel

class Item(BaseModel):
    user: str
    mesasge: bytes


gpt = GPTClient()
tts = TTS()
client = speech.SpeechClient()
freq = 44100
duration = 5
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    audio_channel_count=1,
    language_code="fr-FR",
)
recording_path = "../data/tmp.wav"
recording_input_path = "../data/input.wav"

stt = STT(
    stt_client=client,
    stt_service=speech.RecognitionAudio,
    stt_config=config,
    freq=freq,
    duration=duration,
    recording_path=recording_path,
)
openai.api_key = gpt.api_key


@app.get("/")
async def root():
    return {"message": "welcome to our app to learn english"}


@app.post("/")
async def post_root(file: UploadFile):
    with open(recording_input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    transcript = stt.get_transcript_from_recording(recording_input_path)
    answer = gpt.ask_gpt(transcript)
    audio_path = tts.generate_speech(answer)
    return FileResponse(audio_path)
    # return {"file_name": file.filename, "transcript": transcript, "gpt_answer": answer}


@app.get("/chat")
def answer():
    return {"message": "wecome to chat page"}


@app.post("/chat")
def question(data):
    resp = requests.get(data)
    print(resp)



