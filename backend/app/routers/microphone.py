from fastapi import APIRouter, UploadFile, File
from backend.engine.speech_to_text import STT
from backend.engine.gpt import GPTClient


router = APIRouter()
stt = STT()
gpt = GPTClient()

@router.post("/chat/{chatId}/microphone")
async def upload_audio_file(chatId: str, audio_file: UploadFile = File(...)):
    # Process the audio file here
    # Perform transcription or any other operations
    stt.uploaded_audio = audio_file.file
    trancript = stt.transcript(stt.uploaded_audio)
    gpt.answer(chatId = chatId, user_prompt = trancript)
    # Return a response
    return {"trancript": trancript}