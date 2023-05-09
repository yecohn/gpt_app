from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import moviepy.editor as moviepy
from .routers import user, chat, authentification, topic, lesson
from .oauth2 import get_current_user

message = ""
app = FastAPI()
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(authentification.router)
app.include_router(topic.router)
app.include_router(lesson.router)


# meir = UserInfo("Meir Lejzerowicz", mongo_client)


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
    return {"message": "welcome to our app to learn french"}


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
