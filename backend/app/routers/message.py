from fastapi import APIRouter
from googletrans import Translator

router = APIRouter()
translator = Translator()


@router.post("/translate", status_code=200)
async def translate(
    word: str,
):
    translationObject = translator.translate(word)
    print(translationObject.text)
    translation = translationObject.text
    return {'translation': translation}