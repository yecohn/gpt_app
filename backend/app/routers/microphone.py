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
    tts.generate_speech(answer)



    # response = requests.post(url, data=audio_data, headers=headers)

@router.get('/chat/{chatId}/microphone/download', response_class=FileResponse)
async def download_audio_file(chatId: str):
    
    filename = 'temp.wav'
    headers = {'Content-Disposition': f'attachment; filename={filename}'}
    return FileResponse(tts.audio_path, headers=headers, media_type='audio/m4a')
    # url = 'http://35.236.62.168/chat/' + chatId + '/microphone/audio/answer'
    # 

    # if response.status_code == 200:
    #     audio_url = response.json()['audio_url']
    #     return {'audio_url': audio_url, 'status': 'success'}
    # else:
    #     raise Exception('Failed to upload audio file')
    
    
    
    
    
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