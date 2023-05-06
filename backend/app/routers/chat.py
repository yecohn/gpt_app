from fastapi import APIRouter
from fastapi import UploadFile, File, Depends
from backend.db.sql.sql_connector import access_sql
from backend.db.sql.tables import User
from backend.db.mongo.mongo_connector import access_mongo
import time
import shutil
from backend.engine.gpt import GPTClient
from backend.engine.speech_to_text import STT
from backend.engine.text_to_speech import GCPTTS
from backend.app.users.user import UserInfo
import openai
from google.cloud import speech
from ..oauth2 import get_current_user


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

router = APIRouter()
import os


@router.get("/chat")
def answer():
    return {"message": "wecome to chat page"}


####### Implement this chat with websocket architecture ##############################
@router.get("/chat/{id}")
async def load_chat(
    id: int = Depends(get_current_user),
    mongo_db=Depends(access_mongo),
):
    """load previous chat from database

    Args:
        id (int): id of user

    Returns:
        _type_: _description_
    """
    chat = mongo_db.find(collection_name="chat", query={"user_id": id})
    return {chat: chat}


@router.post("/chat/{id}")
async def question(
    audio: UploadFile, mongo_db=Depends(access_mongo), sql_db=Depends(access_sql)
):
    usrname = sql_db.query(User.username).filter(User.id == id).first()
    start_writing = time.time()
    usr = UserInfo(
        username=usrname,
    )
    gpt = GPTClient(user=usr, db_connector=mongo_db)
    openai.api_key = gpt.api_key
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


##############################################################################