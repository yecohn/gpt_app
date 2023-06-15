from fastapi import APIRouter, UploadFile, File
from backend.engine.speech_to_text import STT
from backend.engine.gpt import GPTClient


router = APIRouter()
stt = STT()
gpt = GPTClient()

@router.post("/chat/{chatId}/microphone")
async def upload_audio_file(chatId: str, file: UploadFile = File(...)):
    # Process the audio file here
    # Perform transcription or any other operations
    print(file)
    try:
        contents = file.file.read()
        with open(file.uri, 'wb') as f:
            f.write(contents)
        
        trancript = stt.transcript(f)
        gpt.answer(chatId = chatId, user_prompt = trancript)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
    # try:
    #     with open(f'audio{audio_file.filename}', 'wb') as f:
    #         f.write(await audio_file.read())

    #     stt.uploaded_audio = f
    #     trancript = stt.transcript(stt.uploaded_audio)
    #     gpt.answer(chatId = chatId, user_prompt = trancript)


    # except Exception as e:
    #     return {"message": "Failed to save the audio file.", "error": str(e)}



    # Return a response
    return {"trancript": trancript, 'status': 'success'}