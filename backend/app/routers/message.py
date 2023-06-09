# from fastapi import APIRouter
# from googletrans import Translator

# router = APIRouter()
# translator = Translator()


# @router.post("/chat/{user_id}/message/translate", status_code=200)
# async def translate(
#     word: str,
# ):
#     print('Endpoint of translation')
#     translationObject = translator.translate(word)
#     print(translationObject.text)
#     translation = translationObject.text
#     return {'translation': translation}