from fastapi import APIRouter
from googletrans import Translator

router = APIRouter()
translator = Translator()


@router.get("/translate/{word}", status_code=200)
async def translate(
    word: str,
):
    translationObject = translator.translate(word)
    translation = translationObject.text
    return translation