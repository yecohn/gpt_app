from fastapi import APIRouter, UploadFile, File
from backend.engine.speech_to_text import STT
from backend.engine.gpt import GPTClient
from fastapi.responses import FileResponse
from backend.engine.text_to_speech import TTS
from fastapi.responses import FileResponse
import tempfile
import os
import requests



tts = TTS()
stt = STT()
gpt = GPTClient()

router = APIRouter()

@router.post("/chat/{chatId}/microphone")
async def upload_audio_file(chatId: str, audio_data: UploadFile = File(...)): #  = File(...)
    # Process the audio file here
    # Perform transcription or any other operations
    temp_dir = tempfile.mkdtemp()
    save_path = os.path.join(temp_dir, 'temp.wav')
    contents = await audio_data.read()

    with open(save_path, 'wb') as f:
        f.write(contents)


    trancript = stt.transcript(save_path)
    answer = gpt.answer(chatId = chatId, user_prompt = trancript)
    audio_answer = tts.generate_speech(answer)
    url =  'http://35.236.62.168/chat/' + chatId + '/microphone/audio/answer'
    with open(audio_answer, 'rb') as audio_file:
        files = {'file': audio_file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        audio_url = response.json()['audio_url']
        return {'audio_url': audio_url, 'status': 'success'}
    else:
        raise Exception('Failed to upload audio file')
    
    
    
    
    
    # return {"message": f"Successfully uploaded {audio_data.filename}"}


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