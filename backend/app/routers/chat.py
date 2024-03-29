
from fastapi import APIRouter, Depends, HTTPException, status, Security, WebSocket
from fastapi import UploadFile, File, Depends
from backend.db.sql.sql_connector import access_sql
from backend.db.mongo.mongo_connector import access_mongo, MongoConnector
from backend.engine.gpt import GPTClient
from backend.engine.speech_to_text import STT
from backend.engine.text_to_speech import GCPTTS
from backend.app.users.user import UserInfo
import openai
from google.cloud import speech
from backend.app.models import MessageChat
from datetime import datetime
import time
import json

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


####### Implement this chat with websocket architecture ##############################
@router.get("/chat/{id}", status_code=200)
async def load_chat(
    id: int,
    mongo_db: MongoConnector = Depends(access_mongo),
):
    """load previous chat from database

    Args:
        id (int): id of user

    Returns:
        _type_: _description_
    """
    # chat = mongo_db.find(collection_name="chat", query={"user_id": id})
    chat = mongo_db.db["chats"].find_one({"user_id": id})
    print(chat)
    res = {"messages": chat["messages"], "user_id": id}
    return res

@router.get("/chat/{id}/reset", status_code=200)
async def reset_chat(
    id: int,
    mongo_db: MongoConnector = Depends(access_mongo),
):
    """load previous chat from database

    Args:
        id (int): id of user
    """
    gpt = GPTClient()
    openai.api_key = gpt.api_key
    mongo_db.db["chats"].delete_one({"user_id": id})
    gpt.start_new_chat()

    answer_json = {
    "user": {"id": id, "name": "ai"},
    'origin': 'system',
    "text": gpt.answer,
    "createdAt": datetime.now(),
    }
    # TO COMPLETE
    new_chat = {
        "user_id": id,
        "chat_id": 1,
        "messages": [answer_json],
        "createdAt": datetime.now(),
    }
    mongo_db.insert_one(new_chat)
    res = {'gpt_first_message': gpt.answer}
    return res


@router.post("/chat/{id}/post", status_code=200)
async def answer(
    messagechat: MessageChat,
    mongo_db: MongoConnector = Depends(access_mongo),
    sql_db=Depends(access_sql),
):
    """answer to a message

    Args:
        id (int): id of user
        message (str): message to answer

    Returns:
        _type_: _description_
    """
    usr = UserInfo(userid=messagechat.user.id, db_connector=sql_db)
    gpt = GPTClient(user=usr, db_connector=mongo_db)
    openai.api_key = gpt.api_key
    question = messagechat.text
    answer = gpt.ask_gpt(question)
    question_json = {
        "user": {"id": messagechat.user.id, "name": usr.username},
        'origin': 'user',
        "text": question,
        "createdAt": messagechat.createdAt,
    }

    answer_json = {
        "user": {"id": messagechat.user.id, "name": "ai"},
        'origin': 'system',
        "text": answer,
        "createdAt": messagechat.createdAt,
    }

    mongo_db.push(
        "chats",
        {"user_id": messagechat.user.id},
        {"$push": {"messages": {"$each": [question_json, answer_json]}}},
    )

    # _ = tts.generate_speech(answer)
    return {"ok": True}


# @router.post("/chat/{id}")
# async def question(
#     audio: UploadFile, mongo_db=Depends(access_mongo), sql_db=Depends(access_sql)
# ):
#     usrname = sql_db.query(User.username).filter(User.id == id).first()
#     start_writing = time.time()
#     usr = UserInfo(
#         username=usrname,
#     )
#     gpt = GPTClient(user=usr, db_connector=mongo_db)
#     openai.api_key = gpt.api_key
#     os.remove(recording_path_video)
#     with open(recording_path_video, "wb") as buffer:
#         shutil.copyfileobj(audio.file, buffer)
#     end_writing = time.time()
#     duration_write = end_writing - start_writing
#     start_converting = time.time()
#     os.system(f"ffmpeg -i {recording_path_video} {recording_input_path} -y")
#     end_converting = time.time()
#     duration_convert = end_converting - start_converting
#     start_transcript = time.time()
#     transcript = stt.get_transcript_from_recording(recording_input_path)
#     end_transcript = time.time()
#     duration_transcript = end_transcript - start_transcript
#     question = transcript
#     start_gpt = time.time()
#     answer = gpt.ask_gpt(question)
#     global message
#     message = answer
#     end_gpt = time.time()
#     duration_gpt = end_gpt - start_gpt
#     print(
#         "write took",
#         duration_write,
#         "seconds",
#         "convert took",
#         duration_convert,
#         "seconds",
#         "transcript took",
#         duration_transcript,
#         "seconds",
#         "gpt took",
#         duration_gpt,
#         "seconds",
#         sep="\n",
#     )
#     _ = tts.generate_speech(answer)
#     return {"answer": answer, "transcript": transcript}


##############################################################################
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = "hello I am a grut "
    while True:
        recieve = await websocket.receive_text()
        print(recieve)
        message = {
            "user": {"id": 1, "name": "AI"},
            "origin": "system",
            "text": data,
            "createdAt": datetime.now(),
        }
        j = json.dumps(message, default=str)
        await websocket.send_text(j)
