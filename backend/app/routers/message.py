from fastapi import APIRouter, Depends
from googletrans import Translator
# from google_trans_new import google_translator
from backend.app.models import TranslationInfo
import json

router = APIRouter()
# translator = google_translator()
translator = Translator()

@router.post("/chat/{user_id}/message/translate", status_code=200)
async def translate(
    info: TranslationInfo,
):
    # info = json.loads(info)
    word = info['word']
    print(f'Endpoint of translation called with word: {word} of type {type(word)}')
    print('Translation in progress...') 
    translationObject = translator.translate(word, src='he')#, lang_tgt='en', lang_src='es')
    print(translationObject)
    return {'translation': translationObject.text}