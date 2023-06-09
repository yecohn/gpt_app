from fastapi import APIRouter, Depends
from googletrans import Translator
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
    translationObject = translator.translate(word)
    print(f'Translation: {translationObject.text}')
    translation = translationObject.text
    return {'translation': translation}