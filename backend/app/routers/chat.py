from fastapi import APIRouter
from backend.engine.gpt import GPTClient
from backend.app.models import MessageChat


router = APIRouter()
gpt = GPTClient()

@router.get("/chat/{id}", status_code=200)
async def load_chat(id: str):

    chat = gpt.load_chat(chatId = id)
    res = {"messages": chat["messages"], "user_id": id}
    return res


@router.post("/chat/{id}/post", status_code=200)
async def answer(id: str, messagechat: MessageChat):

    chatId = id
    gpt.answer(chatId = chatId, user_prompt = messagechat.text)
    res = {"message": "message posted", "success": True}
    return res



@router.get("/chat/{id}/reset", status_code=200)
async def reset_chat(id: str):
    chatId = id
    gpt.reset_chat(chatId = chatId)
    res = {"message": "chat reset", "success": True}
    return res




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

# tts = GCPTTS(language="fr-FR", speaker="fr-FR-Wavenet-A")
# client = speech.SpeechClient()
# freq = 44100
# duration = 5
# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     audio_channel_count=1,
#     language_code="fr-FR",
# )

# recording_path = "./data/tmp.wav"
# recording_path_video = "./data/tmp.webm"
# recording_input_path = "./data/input.wav"
# stt = STT(
#     stt_client=client,
#     stt_service=speech.RecognitionAudio,
#     stt_config=config,
#     freq=freq,
#     duration=duration,
#     recording_path=recording_path,
# )



##############################################################################
# from fastapi import WebSocket
# from fastapi.responses import HTMLResponse


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var ws = new WebSocket("ws://localhost:8000/ws");
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """


# @router.get("/")
# async def get():
#     return HTMLResponse(html)


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     data = "hello I am a grut "
#     while True:
#         recieve = await websocket.receive_text()
#         print(recieve)
#         message = {
#             "user": {"id": 1, "name": "AI"},
#             "origin": "system",
#             "text": data,
#             "createdAt": datetime.now(),
#         }
#         j = json.dumps(message, default=str)
#         await websocket.send_text(j)
