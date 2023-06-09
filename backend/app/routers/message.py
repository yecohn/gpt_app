from fastapi import APIRouter, Depends
from googletrans import Translator
from google_trans_new import google_translator
from backend.app.models import TranslationInfo

router = APIRouter()
translator = Translator()


@router.post("/chat/{user_id}/message/translate", status_code=200)
async def translate(
    info: TranslationInfo = Depends(),
):
    word = info.word
    print(f'Endpoint of translation called with word: {word} of type {type(word)}')
    print('Translation in progress...')
    translation = translator.translate(word, lang_tgt='en')
    print(f'Translation: {translation}')
    return {'translation': translation}