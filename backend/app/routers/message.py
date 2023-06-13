from fastapi import APIRouter
from googletrans import Translator
from backend.app.models import TranslationInfo

router = APIRouter()
# translator = google_translator()
translator = Translator()

@router.post("/chat/{chatId}/message/translate", status_code=200)
async def translate(
    info: TranslationInfo,
):
    # info = json.loads(info)
    print(info)
    word = info.word
    print(f'Endpoint of translation called with word: {word} of type {type(word)}')
    print('Translation in progress...') 
    translationObject = translator.translate(word)#, lang_tgt='en', lang_src='es')
    print(translationObject)
    return {'translation': translationObject.text}